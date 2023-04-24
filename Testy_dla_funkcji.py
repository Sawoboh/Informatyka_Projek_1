# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 23:03:45 2023

@author: Sawob
"""
import pytest
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
        test_dms_d_m_s = Transformacje()
        assert test_dms_d_m_s.dms(1) == "57°17′44.80625″"
        
        
    def test_dms_0d_0m_0s(self):
        test_dms_0d_0m_0s = Transformacje()
        assert test_dms_0d_0m_0s.dms(0) == "0°00′00.00000″"
        
        
    def test_dms_d_0m_s(self):
        test_dms_d_0m_s = Transformacje()
        assert test_dms_d_0m_s.dms(0.001) == "0°03′26.26481″"
        
        
    def test_dms_d_m_0s(self):
        test_dms_d_m_0s = Transformacje()
        assert test_dms_d_m_0s.dms(0.0111) == "0°38′09.53935″"
        
        
    def test_dms_d_0m_0s(self):
        test_dms_d_0m_0s = Transformacje()
        assert test_dms_d_0m_0s.dms(np.pi) == "180°00′00.00000″"

        
    def test_get_np(self):
        test_get_np = Transformacje()
        assert test_get_np.get_np(0) == 6378137.0
        assert np.isclose(test_get_np.get_np(np.pi/4),6388838)
        
        
    def test_hirvonen_radiany(self):
        test_hirvonen_radiany = Transformacje()
        f, l, h = test_hirvonen_radiany.hirvonen(100, 100, 100, output="radiany")
        assert np.isclose(f, -0.00234983317179)
        assert np.isclose(l, 0.7853981633974483)
        assert np.isclose(h, -6377995.69613)
        
        
    def test_hirvonen_dec_degree(self):
        test_hirvonen_dec_degree = Transformacje()
        f, l, h = test_hirvonen_dec_degree.hirvonen(3664940.500, 1409153.590, 5009571.170)
        assert np.isclose(f, 52.09727221932659)
        assert np.isclose(l, 21.031533332797768)
        assert np.isclose(h, 141.39866239)
        
    
    def test_hirvonen_dms(self):
        test_hirvonen_dms = Transformacje()
        f, l, h = test_hirvonen_dms.hirvonen(3664940.500, 1409153.590, 5009571.170, "dms")
        assert f == "52°05′50.17999″"
        assert l == "21°01′53.52000″"
        assert np.isclose(h, 141.39866239)
        