# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 23:03:45 2023

@author: Sawob
"""
import pytest
import math as m
import Transformacje_Projekt   
import numpy as np
from Transformacje_Projekt import Transformacje

class Test_Transoframcje:

    def test_init_WGS84(self):
        test_init_WGS84 = Transformacje('WGS84')
        assert isinstance(test_init_WGS84, Transformacje)
        assert test_init_WGS84.e2 == 0.00669437999013
        assert test_init_WGS84.a == 6378137.000
        
        
    def test_init_GRS80(self):
        test_init_GRS80 = Transformacje('GRS80')
        assert isinstance(test_init_GRS80,Transformacje)
        assert test_init_GRS80.e2 == 0.00669438002290
        assert test_init_GRS80.a == 6378137.000


    def test_init_Krasowski(self):
        test_init_Krasowski = Transformacje('Krasowski')
        assert isinstance(test_init_Krasowski, Transformacje)
        assert test_init_Krasowski.e2 == 0.00669342162296
        assert test_init_Krasowski.a == 6378245.000


    def test_init_invalid(self):
        with pytest.raises(NotImplementedError) as excinfo:
            test_init_invalid = Transformacje('ASDF')
        assert "ASDF  jest nieobsługiwalną elipsoidą - przykładowe elipsoidy WGS84, GRS80, Krasowski." in str(excinfo.value)


    def test_dms_d_m_s(self):
        test_dms_d_m_s_GRS80 = Transformacje("GRS80")
        assert test_dms_d_m_s_GRS80.dms(1) == " 57°17′44.80625″"
        
        test_dms_0d_0m_0s_GRS80 = Transformacje("GRS80")
        assert test_dms_0d_0m_0s_GRS80.dms(0) == "  0°00′00.00000″"
        
        test_dms_d_0m_s_GRS80 = Transformacje("GRS80")
        assert test_dms_d_0m_s_GRS80.dms(0.001) == "  0°03′26.26481″"
        
        test_dms_d_m_0s_GRS80 = Transformacje("GRS80")
        assert test_dms_d_m_0s_GRS80.dms(0.0111) == "  0°38′09.53935″"
        
        test_dms_d_m_0s_GRS80 = Transformacje("GRS80")
        assert test_dms_d_m_0s_GRS80.dms(0.2) == " 11°27′32.96125″"
    
        test_dms_d_0m_0s_GRS80 = Transformacje("GRS80")
        assert test_dms_d_0m_0s_GRS80.dms(np.pi) == "180°00′00.00000″"
        
        test_dms_d_m_s_WGS84 = Transformacje("WGS84")
        assert test_dms_d_m_s_WGS84.dms(1) == " 57°17′44.80625″"
        
        test_dms_0d_0m_0s_WGS84 = Transformacje("WGS84")
        assert test_dms_0d_0m_0s_WGS84.dms(0) == "  0°00′00.00000″"
        
        test_dms_d_0m_s_WGS84 = Transformacje("WGS84")
        assert test_dms_d_0m_s_WGS84.dms(0.001) == "  0°03′26.26481″"
        
        test_dms_d_m_0s_WGS84 = Transformacje("WGS84")
        assert test_dms_d_m_0s_WGS84.dms(0.0111) == "  0°38′09.53935″"
        
        test_dms_d_m_0s_WGS84 = Transformacje("WGS84")
        assert test_dms_d_m_0s_WGS84.dms(0.2) == " 11°27′32.96125″"
    
        test_dms_d_0m_0s_WGS84 = Transformacje("WGS84")
        assert test_dms_d_0m_0s_WGS84.dms(np.pi) == "180°00′00.00000″"
        
        test_dms_d_m_s_Krasowski = Transformacje("Krasowski")
        assert test_dms_d_m_s_Krasowski.dms(1) == " 57°17′44.80625″"
        
        test_dms_0d_0m_0s_Krasowski = Transformacje("Krasowski")
        assert test_dms_0d_0m_0s_Krasowski.dms(0) == "  0°00′00.00000″"
        
        test_dms_d_0m_s_Krasowski = Transformacje("Krasowski")
        assert test_dms_d_0m_s_Krasowski.dms(0.001) == "  0°03′26.26481″"
        
        test_dms_d_m_0s_Krasowski = Transformacje("Krasowski")
        assert test_dms_d_m_0s_Krasowski.dms(0.0111) == "  0°38′09.53935″"
        
        test_dms_d_m_0s_Krasowski = Transformacje("Krasowski")
        assert test_dms_d_m_0s_Krasowski.dms(0.2) == " 11°27′32.96125″"
    
        test_dms_d_0m_0s_Krasowski = Transformacje("Krasowski")
        assert test_dms_d_0m_0s_Krasowski.dms(np.pi) == "180°00′00.00000″"

        
    def test_get_np_GRS80_WGS84_Krasowski(self):
        test_get_np_GRS80 = Transformacje("GRS80")
        assert test_get_np_GRS80.get_np(0) == 6378137.0
        assert np.allclose(test_get_np_GRS80.get_np(4), 6390399.8213711865, rtol=1e-05, atol=1e-08)
        
        test_get_np_WGS84 = Transformacje("WGS84")
        assert test_get_np_WGS84.get_np(0) == 6378137.0
        assert np.allclose(test_get_np_WGS84.get_np(4), 6390399.821310985, rtol=1e-05, atol=1e-08)
        
        test_get_np_Krasowski = Transformacje("Krasowski")
        assert test_get_np_Krasowski.get_np(0) == 6378245.0
        assert np.allclose(test_get_np_Krasowski.get_np(4), 6390506.268315188, rtol=1e-05, atol=1e-08)
        
        
    def test_hirvonen_radiany_GRS80_WGS84_Krasowski(self):
        test_hirvonen_radiany_GRS80 = Transformacje("GRS80")
        f, l, h = test_hirvonen_radiany_GRS80.hirvonen(3664940.500, 1409153.590, 5009571.170, output="radiany")
        assert np.allclose(f, 0.909268931535023, rtol=1e-12, atol=1e-14)
        assert np.allclose(l, 0.367069503400257, rtol=1e-12, atol=1e-14)
        assert np.allclose(h, 141.3986624, rtol=1e-04, atol=1e-06)
        
        test_hirvonen_radiany_WGS84 = Transformacje("WGS84")
        f, l, h = test_hirvonen_radiany_WGS84.hirvonen(3664940.500, 1409153.590, 5009571.170, output="radiany")
        assert np.allclose(f, 0.909268931519064, rtol=1e-12, atol=1e-14)
        assert np.allclose(l, 0.367069503400257, rtol=1e-12, atol=1e-14)
        assert np.allclose(h, 141.3985972, rtol=1e-04, atol=1e-06)
        
        test_hirvonen_radiany_Krasowski = Transformacje("Krasowski")
        f, l, h = test_hirvonen_radiany_Krasowski.hirvonen(3664940.500, 1409153.590, 5009571.170, output="radiany")
        assert np.allclose(f, 0.909268519897417, rtol=1e-12, atol=1e-14)
        assert np.allclose(l, 0.367069503400257, rtol=1e-12, atol=1e-14)
        assert np.allclose(h, 31.7170106, rtol=1e-04, atol=1e-06)
        
        
    def test_hirvonen_dec_degree_GRS80_WGS84_Krasowski(self):
        test_hirvonen_dec_degree_GRS80 = Transformacje("GRS80")
        f, l, h = test_hirvonen_dec_degree_GRS80.hirvonen(3664940.500, 1409153.590, 5009571.170)
        assert np.allclose(f, 52.097272219326591, rtol=1e-12, atol=1e-14)
        assert np.allclose(l, 21.031533332797768, rtol=1e-12, atol=1e-14)
        assert np.allclose(h, 141.3986624, rtol=1e-04, atol=1e-06)
        
        test_hirvonen_dec_degree_WGS84 = Transformacje("WGS84")
        f, l, h = test_hirvonen_dec_degree_WGS84.hirvonen(3664940.500, 1409153.590, 5009571.170)
        assert np.allclose(f, 52.097272218412265, rtol=1e-12, atol=1e-14)
        assert np.allclose(l, 21.031533332797768, rtol=1e-12, atol=1e-14)
        assert np.allclose(h, 141.3985972, rtol=1e-04, atol=1e-06)
        
        test_hirvonen_dec_degree_Krasowski = Transformacje("Krasowski")
        f, l, h = test_hirvonen_dec_degree_Krasowski.hirvonen(3664940.500, 1409153.590, 5009571.170)
        assert np.allclose(f, 52.097248634229103, rtol=1e-12, atol=1e-14)
        assert np.allclose(l, 21.031533332797768, rtol=1e-12, atol=1e-14)
        assert np.allclose(h, 31.7170106, rtol=1e-04, atol=1e-06)
        
    
    def test_hirvonen_dms_GRS80_WGS84_Krasowski(self):
        test_hirvonen_dms_GRS80 = Transformacje("GRS80")
        f, l, h = test_hirvonen_dms_GRS80.hirvonen(3664940.500, 1409153.590, 5009571.170, output="dms")
        assert f == " 52°05′50.17999″"
        assert l == " 21°01′53.52000″"
        assert np.allclose(h, 141.3986624, rtol=1e-04, atol=1e-06)
        
        test_hirvonen_dms_WGS84 = Transformacje("WGS84")
        f, l, h = test_hirvonen_dms_WGS84.hirvonen(3664940.500, 1409153.590, 5009571.170, output="dms")
        assert f == " 52°05′50.17999″"
        assert l == " 21°01′53.52000″"
        assert np.allclose(h, 141.3985972, rtol=1e-04, atol=1e-06)
        
        test_hirvonen_dms_Krasowski = Transformacje("Krasowski")
        f, l, h = test_hirvonen_dms_Krasowski.hirvonen(3664940.500, 1409153.590, 5009571.170, output="dms")
        assert f == " 52°05′50.09508″"
        assert l == " 21°01′53.52000″"
        assert np.allclose(h, 31.7170106, rtol=1e-04, atol=1e-06)
    
    
    def test_flh2XYZ_GRS80_WGS84_Krasowski(self):
        test_flh2XYZ_GRS80 = Transformacje("GRS80")
        X, Y, Z = test_flh2XYZ_GRS80.flh2XYZ(2, 4, 5)
        assert np.allclose(X, 6358755.1628596968948841094971, rtol=1e-14, atol=1e-22)
        assert np.allclose(Y, 444647.4764681159867905080318, rtol=1e-14, atol=1e-22)
        assert np.allclose(Z, 221104.7198013129527680575848, rtol=1e-14, atol=1e-22)
        
        test_flh2XYZ_WGS84 = Transformacje("WGS84")
        X, Y, Z = test_flh2XYZ_WGS84.flh2XYZ(2, 4, 5)
        assert np.allclose(X, 6358755.1628595693036913871765, rtol=1e-14, atol=1e-22)
        assert np.allclose(Y, 444647.4764681070810183882713, rtol=1e-14, atol=1e-22)
        assert np.allclose(Z, 221104.7198086029384285211563, rtol=1e-14, atol=1e-22)
        
        test_flh2XYZ_Krasowski = Transformacje("Krasowski")
        X, Y, Z = test_flh2XYZ_Krasowski.flh2XYZ(2, 4, 5)
        assert np.allclose(X, 6358862.8308742623776197433472, rtol=1e-14, atol=1e-22)
        assert np.allclose(Y, 444655.0053491228609345853329, rtol=1e-14, atol=1e-22)
        assert np.allclose(Z, 221108.6769394139992073178291, rtol=1e-14, atol=1e-22)
        
        
    def test_flh2PL92_GRS80_WGS84_Krasowski(self):
        test_flh2PL92_GRS80 = Transformacje("GRS80")
        X, Y = test_flh2PL92_GRS80.flh2PL92(48.9, 13.5)
        assert np.allclose(X, 129306.4595286045223474502563, rtol=1e-14, atol=1e-22)
        assert np.allclose(Y, 97116.4720873863552697002888, rtol=1e-14, atol=1e-22)
        
        test_flh2PL92_WGS84 = Transformacje("WGS84")
        X, Y = test_flh2PL92_WGS84.flh2PL92(48.9, 13.5)
        assert np.allclose(X, 129306.4596510492265224456787, rtol=1e-14, atol=1e-22)
        assert np.allclose(Y, 97116.4720911530894227325916, rtol=1e-14, atol=1e-22)
        
        test_flh2PL92_Krasowski = Transformacje("Krasowski")
        X, Y = test_flh2PL92_Krasowski.flh2PL92(48.9, 13.5)
        assert np.allclose(X, 129401.9742508260533213615417, rtol=1e-14, atol=1e-22)
        assert np.allclose(Y, 97109.7602860580664128065109, rtol=1e-14, atol=1e-22)

        
    def test_flh2PL92_invalid_f_l_GRS80_WGS84_Krasowski(self):
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL92_invalid_l_GRS80 = Transformacje('GRS80')
            X, Y = test_flh2PL92_invalid_l_GRS80.flh2PL92(49, 12.5)
        assert "12°30′00.00000″ ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL1992" in str(excinfo.value)
       
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL92_invalid_f_GRS80 = Transformacje('GRS80')
            X, Y = test_flh2PL92_invalid_f_GRS80.flh2PL92(12.5, 21)
        assert "12°30′00.00000″ ten równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL1992" in str(excinfo.value)     
        
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL92_invalid_l_f_GRS80 = Transformacje('GRS80')
            X, Y = test_flh2PL92_invalid_l_f_GRS80.flh2PL92(12.5, 12.5)
        assert "12°30′00.00000″ ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL1992" in str(excinfo.value)
        
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL92_invalid_l_WGS84 = Transformacje('WGS84')
            X, Y = test_flh2PL92_invalid_l_WGS84.flh2PL92(49, 12.5)
        assert "12°30′00.00000″ ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL1992" in str(excinfo.value)
       
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL92_invalid_f_WGS84 = Transformacje('WGS84')
            X, Y = test_flh2PL92_invalid_f_WGS84.flh2PL92(12.5, 21)
        assert "12°30′00.00000″ ten równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL1992" in str(excinfo.value)     
        
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL92_invalid_l_f_WGS84 = Transformacje('WGS84')
            X, Y = test_flh2PL92_invalid_l_f_WGS84.flh2PL92(12.5, 12.5)
        assert "12°30′00.00000″ ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL1992" in str(excinfo.value)
        
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL92_invalid_l_Krasowski = Transformacje('Krasowski')
            X, Y = test_flh2PL92_invalid_l_Krasowski.flh2PL92(49, 12.5)
        assert "12°30′00.00000″ ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL1992" in str(excinfo.value)
       
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL92_invalid_f_Krasowski = Transformacje('Krasowski')
            X, Y = test_flh2PL92_invalid_f_Krasowski.flh2PL92(12.5, 21)
        assert "12°30′00.00000″ ten równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL1992" in str(excinfo.value)     
        
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL92_invalid_l_f_Krasowski = Transformacje('Krasowski')
            X, Y = test_flh2PL92_invalid_l_f_Krasowski.flh2PL92(12.5, 12.5)
        assert "12°30′00.00000″ ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL1992" in str(excinfo.value)
        
        
    def test_flh2PL00_GRS80_WGS84_Krasowski(self):
        test_flh2PL00_GRS80 = Transformacje("GRS80")
        X, Y = test_flh2PL00_GRS80.flh2PL00(48.9, 13.5)
        assert np.allclose(X, 5419174.3754269238561391830444, rtol=1e-14, atol=1e-22)
        assert np.allclose(Y, 5390032.9063540548086166381836, rtol=1e-14, atol=1e-22)
        
        test_flh2PL00_WGS84 = Transformacje("WGS84")
        X, Y = test_flh2PL00_WGS84.flh2PL00(48.9, 13.5)
        assert np.allclose(X, 5419174.3755495715886354446411, rtol=1e-14, atol=1e-22)
        assert np.allclose(Y, 5390032.9063550820574164390564, rtol=1e-14, atol=1e-22)
        
        test_flh2PL00_Krasowski = Transformacje("Krasowski")
        X, Y = test_flh2PL00_Krasowski.flh2PL00(48.9, 13.5)
        assert np.allclose(X, 5419269.7245272155851125717163, rtol=1e-14, atol=1e-22)
        assert np.allclose(Y, 5390031.0743393180891871452332, rtol=1e-14, atol=1e-22)     
        
        
    def test_flh2PL00_invalid_f_l_GRS80_WGS84_Krasowski(self):
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL00_invalid_l_GRS80 = Transformacje('GRS80')
            X, Y = test_flh2PL00_invalid_l_GRS80.flh2PL00(49, 12.5)
        assert "12°30′00.00000″ ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL2000" in str(excinfo.value)
       
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL00_invalid_f_GRS80 = Transformacje('GRS80')
            X, Y = test_flh2PL00_invalid_f_GRS80.flh2PL00(12.5, 21)
        assert "12°30′00.00000″ ten równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL2000" in str(excinfo.value)     
        
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL00_invalid_l_f_GRS80 = Transformacje('GRS80')
            X, Y = test_flh2PL00_invalid_l_f_GRS80.flh2PL00(12.5, 12.5)
        assert "12°30′00.00000″ ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL2000" in str(excinfo.value)
        
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL00_invalid_l_WGS84 = Transformacje('WGS84')
            X, Y = test_flh2PL00_invalid_l_WGS84.flh2PL00(49, 12.5)
        assert "12°30′00.00000″ ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL2000" in str(excinfo.value)
       
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL00_invalid_f_WGS84 = Transformacje('WGS84')
            X, Y = test_flh2PL00_invalid_f_WGS84.flh2PL00(12.5, 21)
        assert "12°30′00.00000″ ten równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL2000" in str(excinfo.value)     
        
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL00_invalid_l_f_WGS84 = Transformacje('WGS84')
            X, Y = test_flh2PL00_invalid_l_f_WGS84.flh2PL00(12.5, 12.5)
        assert "12°30′00.00000″ ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL2000" in str(excinfo.value)
        
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL00_invalid_l_Krasowski = Transformacje('Krasowski')
            X, Y = test_flh2PL00_invalid_l_Krasowski.flh2PL00(49, 12.5)
        assert "12°30′00.00000″ ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL2000" in str(excinfo.value)
       
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL00_invalid_f_Krasowski = Transformacje('Krasowski')
            X, Y = test_flh2PL00_invalid_f_Krasowski.flh2PL00(12.5, 21)
        assert "12°30′00.00000″ ten równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL2000" in str(excinfo.value)     
        
        with pytest.raises(NotImplementedError) as excinfo:
            test_flh2PL00_invalid_l_f_Krasowski = Transformacje('Krasowski')
            X, Y = test_flh2PL00_invalid_l_f_Krasowski.flh2PL00(12.5, 12.5)
        assert "12°30′00.00000″ ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL2000" in str(excinfo.value)
        
    
    def test_rneu_GRS80_WGS84_Krasowski(self):
        test_rneu_GRS80 = Transformacje("GRS80")
        R = test_rneu_GRS80.rneu(10,10)
        assert np.allclose(R[0,0], -0.171010071662834328698465924390, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[0,1], -0.173648177666930331186634361984, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[0,2],  0.969846310392954102930218596157, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[1,0], -0.030153689607045803394713701095, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[1,1],  0.984807753012208020315654266597, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[1,2],  0.171010071662834328698465924390, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[2,0],  0.984807753012208020315654266597, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[2,1],  0.000000000000000000000000000000, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[2,2],  0.173648177666930331186634361984, rtol=1e-25, atol=1e-30)
        
        test_rneu_WGS84 = Transformacje("WGS84")
        R = test_rneu_WGS84.rneu(10,10)
        assert np.allclose(R[0,0], -0.171010071662834328698465924390, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[0,1], -0.173648177666930331186634361984, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[0,2],  0.969846310392954102930218596157, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[1,0], -0.030153689607045803394713701095, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[1,1],  0.984807753012208020315654266597, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[1,2],  0.171010071662834328698465924390, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[2,0],  0.984807753012208020315654266597, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[2,1],  0.000000000000000000000000000000, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[2,2],  0.173648177666930331186634361984, rtol=1e-25, atol=1e-30)
        
        test_rneu_Krasowski = Transformacje("Krasowski")
        R = test_rneu_Krasowski.rneu(10,10)
        assert np.allclose(R[0,0], -0.171010071662834328698465924390, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[0,1], -0.173648177666930331186634361984, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[0,2],  0.969846310392954102930218596157, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[1,0], -0.030153689607045803394713701095, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[1,1],  0.984807753012208020315654266597, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[1,2],  0.171010071662834328698465924390, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[2,0],  0.984807753012208020315654266597, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[2,1],  0.000000000000000000000000000000, rtol=1e-25, atol=1e-30)
        assert np.allclose(R[2,2],  0.173648177666930331186634361984, rtol=1e-25, atol=1e-30)
        
    
    def test_get_dXYZ_GRS80_WGS84_Krasowski(self):
        test_get_dXYZ_GRS80 = Transformacje("GRS80")
        dXYZ = test_get_dXYZ_GRS80.get_dXYZ(234, 645, 13, 412, 642, 12)
        assert dXYZ[0] == 178
        assert dXYZ[1] == -3
        assert dXYZ[2] == -1
        
        test_get_dXYZ_WGS84 = Transformacje("WGS84")
        dXYZ = test_get_dXYZ_WGS84.get_dXYZ(234, 645, 13, 412, 642, 12)
        assert dXYZ[0] == 178
        assert dXYZ[1] == -3
        assert dXYZ[2] == -1
        
        test_get_dXYZ_Krasowski = Transformacje("Krasowski")
        dXYZ = test_get_dXYZ_Krasowski.get_dXYZ(234, 645, 13, 412, 642, 12)
        assert dXYZ[0] == 178
        assert dXYZ[1] == -3
        assert dXYZ[2] == -1
        
    
    def test_xyz2neu_GRS80_WGS84_Krasowski(self):
        test_xyz2neu_GRS80 = Transformacje("GRS80")
        n, e, u = test_xyz2neu_GRS80.xyz2neu(10, 10, 234, 645, 13, 412, 642, 12)
        assert n == "                              -31.3341394401755799" 
        assert e == "                              -33.8637988837502277"
        assert u == "                              171.9459648572903916"
        
        test_xyz2neu_WGS84 = Transformacje("WGS84")
        n, e, u = test_xyz2neu_WGS84.xyz2neu(10, 10, 234, 645, 13, 412, 642, 12)
        assert n == "                              -31.3341394401755799" 
        assert e == "                              -33.8637988837502277"
        assert u == "                              171.9459648572903916"
        
        test_xyz2neu_Krasowski = Transformacje("Krasowski")
        n, e, u = test_xyz2neu_Krasowski.xyz2neu(10, 10, 234, 645, 13, 412, 642, 12)
        assert n == "                              -31.3341394401755799" 
        assert e == "                              -33.8637988837502277"
        assert u == "                              171.9459648572903916"
        
        
    def test_zamiana_float2string_GRS80_WGS84_Krasowski(self):
        test_zamiana_float2string_GRS80 = Transformacje("GRS80")
        x = test_zamiana_float2string_GRS80.zamiana_float2string(23.2412122)
        z = test_zamiana_float2string_GRS80.zamiana_float2string(0)
        assert x == "               23.241"
        assert z == "                0.000"
        
        test_zamiana_float2string_WGS84 = Transformacje("WGS84")
        x = test_zamiana_float2string_WGS84.zamiana_float2string(23.2412122)
        z = test_zamiana_float2string_WGS84.zamiana_float2string(0)
        assert x == "               23.241"
        assert z == "                0.000"
        
        test_zamiana_float2string_Krasowski = Transformacje("Krasowski")
        x = test_zamiana_float2string_Krasowski.zamiana_float2string(23.2412122)
        z = test_zamiana_float2string_Krasowski.zamiana_float2string(0)
        assert x == "               23.241"
        assert z == "                0.000"
        
    
    def test_wczytanie_pliku_GRS80_WGS84_Krasowski(self):
        test_wczytanie_pliku_GRS80 = Transformacje("GRS80")
        X, Y, Z, C = test_wczytanie_pliku_GRS80.wczytanie_pliku("wsp_inp.txt")
        assert X[0] == 3664940.500
        assert Y[3] == 1409153.560
        assert X[8] == 3664940.515
        assert Z[5] == 5009571.166
        
        test_wczytanie_pliku_GRS80 = Transformacje("GRS80")
        X, Y, Z, C = test_wczytanie_pliku_GRS80.wczytanie_pliku("wsp_inp_Losowe_dane.txt")
        assert X[0] == 12
        assert Y[3] == 1409153.564
        assert X[8] == 12
        assert Z[5] == 1
        
        test_wczytanie_pliku_WGS84 = Transformacje("WGS84")
        X, Y, Z, C = test_wczytanie_pliku_WGS84.wczytanie_pliku("wsp_inp.txt")
        assert X[0] == 3664940.500
        assert Y[3] == 1409153.560
        assert X[8] == 3664940.515
        assert Z[5] == 5009571.166
        
        test_wczytanie_pliku_WGS84 = Transformacje("WGS84")
        X, Y, Z, C = test_wczytanie_pliku_WGS84.wczytanie_pliku("wsp_inp_Losowe_dane.txt")
        assert X[0] == 12
        assert Y[3] == 1409153.564
        assert X[8] == 12
        assert Z[5] == 1
        
        test_wczytanie_pliku_Krasowski = Transformacje("Krasowski")
        X, Y, Z, C = test_wczytanie_pliku_Krasowski.wczytanie_pliku("wsp_inp.txt")
        assert X[0] == 3664940.500
        assert Y[3] == 1409153.560
        assert X[8] == 3664940.515
        assert Z[5] == 5009571.166
        
        test_wczytanie_pliku_Krasowski = Transformacje("GRS80")
        X, Y, Z, C = test_wczytanie_pliku_Krasowski.wczytanie_pliku("wsp_inp_Losowe_dane.txt")
        assert X[0] == 12
        assert Y[3] == 1409153.564
        assert X[8] == 12
        assert Z[5] == 1
        
    
    def test_zapisaniePliku_GRS80_WGS84_Krasowski(self):
        test_zapisaniePliku_GRS80 = Transformacje("GRS80")
        X = [3664940.500, 3664940.510]
        Y = [1409153.590, 1409153.580]
        Z = [5009571.170, 5009571.167]
        x92 = [472071.341, 472071.334]
        y92 = [639114.491, 639114.478]
        x00 = [5773722.721, 5773722.715]
        y00 = [7502160.783, 7502160.770]
        N = [-0.0072609883070758, -0.0063760985828238]
        E = [-0.0102657604124220, -0.0129226474742650]
        U = [0.0069204196245229, 0.0011621283046183]
        f,l,h = test_zapisaniePliku_GRS80.hirvonen(X[0], Y[0], Z[0], output="dms")
        f1,l1,h1 = test_zapisaniePliku_GRS80.hirvonen(X[1], Y[1], Z[1], output="dms")
        X[0] = test_zapisaniePliku_GRS80.zamiana_float2string(X[0])
        X[1] = test_zapisaniePliku_GRS80.zamiana_float2string(X[1])
        Y[0] = test_zapisaniePliku_GRS80.zamiana_float2string(Y[0])
        Y[1] = test_zapisaniePliku_GRS80.zamiana_float2string(Y[1])
        Z[0] = test_zapisaniePliku_GRS80.zamiana_float2string(Z[0])
        Z[1] = test_zapisaniePliku_GRS80.zamiana_float2string(Z[1])
        h = test_zapisaniePliku_GRS80.zamiana_float2string(h)
        h1 = test_zapisaniePliku_GRS80.zamiana_float2string(h1)
        x92[0] = test_zapisaniePliku_GRS80.zamiana_float2string(x92[0])
        x92[1] = test_zapisaniePliku_GRS80.zamiana_float2string(x92[1])
        y92[0] = test_zapisaniePliku_GRS80.zamiana_float2string(y92[0])
        y92[1] = test_zapisaniePliku_GRS80.zamiana_float2string(y92[1])
        x00[0] = test_zapisaniePliku_GRS80.zamiana_float2string(x00[0])
        x00[1] = test_zapisaniePliku_GRS80.zamiana_float2string(x00[1])
        y00[0] = test_zapisaniePliku_GRS80.zamiana_float2string(y00[0])
        y00[1] = test_zapisaniePliku_GRS80.zamiana_float2string(y00[1])
        assert X[0] == "          3664940.500"
        assert Y[1] == "          1409153.580"
        assert Z[0] == "          5009571.170"
        assert f == " 52°05′50.17999″"
        assert l1 == " 21°01′53.51932″"
        assert h == "              141.399"
        assert x92[0] == "           472071.341"
        assert y92[1] == "           639114.478"
        assert x00[1] == "          5773722.715"
        assert y00[1] == "          7502160.770"
        assert N[0] == -0.0072609883070758
        assert E[0] == -0.0102657604124220
        assert U[0] == 0.0069204196245229
        
        test_zapisaniePliku_WGS84 = Transformacje("WGS84")
        X = [3664940.500, 3664940.510]
        Y = [1409153.590, 1409153.580]
        Z = [5009571.170, 5009571.167]
        x92 = [472071.341, 472071.334]
        y92 = [639114.491, 639114.478]
        x00 = [5773722.721, 5773722.715]
        y00 = [7502160.783, 7502160.770]
        N = [-0.0072609883070758, -0.0063760985828238]
        E = [-0.0102657604124220, -0.0129226474742650]
        U = [0.0069204196245229, 0.0011621283046183]
        f,l,h = test_zapisaniePliku_WGS84.hirvonen(X[0], Y[0], Z[0], output="dms")
        f1,l1,h1 = test_zapisaniePliku_WGS84.hirvonen(X[1], Y[1], Z[1], output="dms")
        X[0] = test_zapisaniePliku_WGS84.zamiana_float2string(X[0])
        X[1] = test_zapisaniePliku_WGS84.zamiana_float2string(X[1])
        Y[0] = test_zapisaniePliku_WGS84.zamiana_float2string(Y[0])
        Y[1] = test_zapisaniePliku_WGS84.zamiana_float2string(Y[1])
        Z[0] = test_zapisaniePliku_WGS84.zamiana_float2string(Z[0])
        Z[1] = test_zapisaniePliku_WGS84.zamiana_float2string(Z[1])
        h = test_zapisaniePliku_WGS84.zamiana_float2string(h)
        h1 = test_zapisaniePliku_WGS84.zamiana_float2string(h1)
        x92[0] = test_zapisaniePliku_WGS84.zamiana_float2string(x92[0])
        x92[1] = test_zapisaniePliku_WGS84.zamiana_float2string(x92[1])
        y92[0] = test_zapisaniePliku_WGS84.zamiana_float2string(y92[0])
        y92[1] = test_zapisaniePliku_WGS84.zamiana_float2string(y92[1])
        x00[0] = test_zapisaniePliku_WGS84.zamiana_float2string(x00[0])
        x00[1] = test_zapisaniePliku_WGS84.zamiana_float2string(x00[1])
        y00[0] = test_zapisaniePliku_WGS84.zamiana_float2string(y00[0])
        y00[1] = test_zapisaniePliku_WGS84.zamiana_float2string(y00[1])
        assert X[0] == "          3664940.500"
        assert Y[1] == "          1409153.580"
        assert Z[0] == "          5009571.170"
        assert f == " 52°05′50.17999″"
        assert l1 == " 21°01′53.51932″"
        assert h == "              141.399"
        assert x92[0] == "           472071.341"
        assert y92[1] == "           639114.478"
        assert x00[1] == "          5773722.715"
        assert y00[1] == "          7502160.770"
        assert N[0] == -0.0072609883070758
        assert E[0] == -0.0102657604124220
        assert U[0] ==  0.0069204196245229
        
        test_zapisaniePliku_Krasowski = Transformacje("Krasowski")
        X = [3664940.500, 3664940.510]
        Y = [1409153.590, 1409153.580]
        Z = [5009571.170, 5009571.167]
        x92 = [472071.341, 472071.334]
        y92 = [639114.491, 639114.478]
        x00 = [5773722.721, 5773722.715]
        y00 = [7502160.783, 7502160.770]
        N = [-0.0072609883070758, -0.0063760985828238]
        E = [-0.0102657604124220, -0.0129226474742650]
        U = [0.0069204196245229, 0.0011621283046183]
        f,l,h = test_zapisaniePliku_Krasowski.hirvonen(X[0], Y[0], Z[0], output="dms")
        f1,l1,h1 = test_zapisaniePliku_Krasowski.hirvonen(X[1], Y[1], Z[1], output="dms")
        X[0] = test_zapisaniePliku_Krasowski.zamiana_float2string(X[0])
        X[1] = test_zapisaniePliku_Krasowski.zamiana_float2string(X[1])
        Y[0] = test_zapisaniePliku_Krasowski.zamiana_float2string(Y[0])
        Y[1] = test_zapisaniePliku_Krasowski.zamiana_float2string(Y[1])
        Z[0] = test_zapisaniePliku_Krasowski.zamiana_float2string(Z[0])
        Z[1] = test_zapisaniePliku_Krasowski.zamiana_float2string(Z[1])
        h = test_zapisaniePliku_Krasowski.zamiana_float2string(h)
        h1 = test_zapisaniePliku_Krasowski.zamiana_float2string(h1)
        x92[0] = test_zapisaniePliku_Krasowski.zamiana_float2string(x92[0])
        x92[1] = test_zapisaniePliku_Krasowski.zamiana_float2string(x92[1])
        y92[0] = test_zapisaniePliku_Krasowski.zamiana_float2string(y92[0])
        y92[1] = test_zapisaniePliku_Krasowski.zamiana_float2string(y92[1])
        x00[0] = test_zapisaniePliku_Krasowski.zamiana_float2string(x00[0])
        x00[1] = test_zapisaniePliku_Krasowski.zamiana_float2string(x00[1])
        y00[0] = test_zapisaniePliku_Krasowski.zamiana_float2string(y00[0])
        y00[1] = test_zapisaniePliku_Krasowski.zamiana_float2string(y00[1])

        assert Y[1] == "          1409153.580"
        assert Z[0] == "          5009571.170"
        assert f == " 52°05′50.09508″"
        assert l1 == " 21°01′53.51932″"
        assert h == "               31.717"
        assert x92[0] == "           472071.341"
        assert y92[1] == "           639114.478"
        assert x00[1] == "          5773722.715"
        assert y00[1] == "          7502160.770"
        assert N[0] == -0.0072609883070758
        assert E[0] == -0.0102657604124220
        assert U[0] ==  0.0069204196245229