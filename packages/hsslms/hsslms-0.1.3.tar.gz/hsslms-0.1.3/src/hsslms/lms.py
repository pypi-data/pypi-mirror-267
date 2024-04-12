# -*- coding: utf-8 -*-
"""Leighton-Micali Signatures

For reference see RFC 8554, section 5.
"""
from os import cpu_count
from secrets import token_bytes
from multiprocessing import Pool
from .utils import LMOTS_ALGORITHM_TYPE, LMS_ALGORITHM_TYPE
from .utils import INVALID, FAILURE
from .utils import D_LEAF, D_INTR
from .utils import u32str, strTou32
from .lmots import LM_OTS_Priv, LM_OTS_Pub


class LMS_Pub:
    """A class used to hold the public key of Leighton-Micali Signatures (LMS)
    
    For a reference see RFC 8554, section 5.

    Args:
        pubkey (bytes): u32str(type) || u32str(otstype) || I || T[1]
        
    Raises:
        INVALID: If the public is invalid.
    """
    def __init__(self, pubkey):
        if len(pubkey) < 8:
            raise INVALID
        try:
            self.pubtype = LMS_ALGORITHM_TYPE(strTou32(pubkey[:4]))
        except ValueError:
            raise INVALID
        self.H, self.m, self.h = self.pubtype.H, self.pubtype.m, self.pubtype.h
        if len(pubkey) != 24+self.m:
            raise INVALID
        try:
            self.otspubtype = LMOTS_ALGORITHM_TYPE(strTou32(pubkey[4:4+4]))
        except ValueError:
            raise INVALID
        self.I = pubkey[8:8+16]
        self.T1 = pubkey[24:]
        self.pubkey = pubkey
        
    def _len_pubkey(pubkey):
        """Computes the correct length of a given public key
        
        Args:
            pubkey (bytes): Representation of a public key
            
        Raises:
            INVALID: If the byte string is malformed.
        
        Returns:
            int: Length of the public key.
        """
        if len(pubkey) < 4:
            raise INVALID('Malformed public key.')
        try:
            return 24 + LMS_ALGORITHM_TYPE(strTou32(pubkey[:4])).m
        except:
            raise INVALID('Malformed public key.')
        
    def _algo6b(self, message, signature):
        if len(signature) < 8:
            raise INVALID
        q = strTou32(signature[:4])
        otssigtype = LMOTS_ALGORITHM_TYPE(strTou32(signature[4:4+4]))
        if self.otspubtype != otssigtype:
            raise INVALID
        n, p = otssigtype.n, otssigtype.p
        if len(signature) < 12 + n*(p+1):
            raise INVALID
        lmots_signature = signature[4:8 + n*(p+1)]
        sigtype = LMS_ALGORITHM_TYPE(strTou32(signature[8+n*(p+1):12+n*(p+1)]))
        if self.pubtype != sigtype:
            raise INVALID
        if q >= 2**self.h or len(signature) != 12+n*(p+1)+self.m*self.h:
            raise INVALID
        OTS_PUB = LM_OTS_Pub(lmots_signature[:4] + self.I + u32str(q)  + b'\x00'*n)
        Kc = OTS_PUB._algo4b(message, lmots_signature)
        node_num = 2**self.h + q
        tmp = self.H(self.I + u32str(node_num) + D_LEAF + Kc).digest()[:self.m]
        i = 0
        while node_num > 1:
            path = signature[12+n*(p+1)+i*self.m:12+n*(p+1)+(i+1)*self.m]
            if node_num % 2 == 1:
                tmp = self.H(self.I + u32str(node_num//2) + D_INTR + path + tmp).digest()[:self.m]
            else:
                tmp = self.H(self.I + u32str(node_num//2) + D_INTR + tmp + path).digest()[:self.m]
            node_num >>= 1
            i += 1
        return tmp  # Tc
        
    def verify(self, message, signature):
        """Signature Verification of LMS

        Tries to verify the signature of a message with the public key associated
        with the class.
        
        Args:
            message (bytes, BufferedReader): Message to be verified with `signature`
            signature (bytes): Signature belonging to the `message`
        
        Raises:
            INVALID: If signature is invalid.
        """
        Tc = self._algo6b(message, signature)
        if Tc != self.T1:
            raise INVALID
            
    def _len_signature(signature):
        """Computes the correct length of a signature in an even longer byte string
        
        Args:
            signature (bytes): Signature embedded in an even longer byte string.
        Raises:
            INVALID: If the signature is malformed.
        
        Returns:
            int: the length of a signature
        """
        if len(signature) < 8:
            raise INVALID
        otssigtype = LMOTS_ALGORITHM_TYPE(strTou32(signature[4:4+4]))
        n, p = otssigtype.n, otssigtype.p
        if len(signature) < 12+n*(p+1):
            raise INVALID
        sigtype = LMS_ALGORITHM_TYPE(strTou32(signature[8+n*(p+1):12+n*(p+1)]))
        if len(signature) < 12 + n*(p+1) + sigtype.m * sigtype.h:
            raise INVALID
        return 12 + n*(p+1) + sigtype.m * sigtype.h
                
            
    def get_pubkey(self):
        return self.pubkey
    
    def info(self):
        return """\
lmotstype = {self.otspubtype.name}
lmstype = {self.pubtype.name}
"""
        

class LMS_Priv:
    """A class used to hold the private key of Leighton-Micali Signatures (LMS)
    
    For a reference see RFC 8554, section 5.
    
    This class can be used to generate the belonging public key `LMS_Pub`.

    Args:
        typecode (LMS_ALGORITHM_TYPE): Enumeration of Leighton-Micali Signatures (LMS) algorithm types
        otstypecode (LMOTS_ALGORITHM_TYPE): Enumeration of Leighton-Micali One-Time-Signatures (LMOTS) algorithm types
        num_cores (int, None, optional): the number of CPU cores used for key generation, None=all cores
    """
    def _calc_leafs(H, I, r, h, otstypecode, SEED):
        OTS_PRIV = LM_OTS_Priv(otstypecode, I, r-2**h, SEED)
        return H(I + u32str(r) + D_LEAF + OTS_PRIV.gen_pub_K()).digest()[:otstypecode.n]
    def _calc_knots(H, I, r, Tl, Tr, m):
        return H(I + u32str(r) + D_INTR + Tl + Tr).digest()[:m]
    
    def __init__(self, typecode, otstypecode, num_cores=None):
        if num_cores is None:
            num_cores = cpu_count()
        self.typecode = typecode
        self.otstypecode = otstypecode
        self.H, self.m, self.h = self.typecode.H, self.typecode.m, self.typecode.h
        self.SEED = token_bytes(self.m)
        self.I = token_bytes(16)
        with Pool(num_cores) as p:
            self.T = [None]*(2**(self.h+1))
            self.T[2**self.h : 2**(self.h+1)] = p.starmap(LMS_Priv._calc_leafs, ((self.H, self.I, r, self.h, self.otstypecode, self.SEED) for r in range(2**self.h, 2**(self.h+1))))
            for i in range(self.h-1, -1, -1):
                self.T[2**i : 2**(i+1)] = p.starmap(LMS_Priv._calc_knots, ((self.H, self.I, r, self.T[2*r], self.T[2*r+1], self.m) for r in range(2**i, 2**(i+1))))
        self.q = 0
        
    def sign(self, message):
        """Signature Generation of LMS
        
        Signs a message with the private key associated with the class.
        
        Args:
            message (bytes, BufferedReader): Message to be signed
        
        Raises:
            FAILURE: If a signature has already been computed, or for other
                technical reason
        
        Returns:
            bytes: The signature to `message`.
        """
        if self.q >= 2**self.h:
            raise FAILURE("Private keys exhausted.")
        lmots_signature = LM_OTS_Priv(self.otstypecode, self.I, self.q, self.SEED).sign(message)
        signature = u32str(self.q) + lmots_signature + u32str(self.typecode.value)
        r = 2**self.h + self.q
        for i in range(self.h):
            signature += self.T[r ^ 1]
            r >>= 1
        self.q += 1
        return signature
        
    def gen_pub(self):
        """Computes the public key associated with the private key in this class.
        
        Returns:
            LMS_Pub: The public key belonging to this private key.
        """
        return LMS_Pub(u32str(self.typecode.value) + u32str(self.otstypecode.value) + self.I + self.T[1])
    
    def get_avail_signatures(self):
        """Computes the numbers of availalbe signatures.
        
        Every invokation of the 'sign'-Method reduces this number by one.
        
        Returns:
            int: The remaining number of signatures that can be generated.
        """
        return 2**self.h - self.q
    
