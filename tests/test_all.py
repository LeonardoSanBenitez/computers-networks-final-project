import pytest
import sys
sys.path.append("..")

# Math and ML
import cv2
import numpy as np

# AI modules
import perception
import reasoning
import interaction
import communication

#TODO: improve these tests, now it's ridiculous

class TestPerception():
    def test_instantiation(self):
        bme280 = perception.Sensor_Bme280()
        camera = perception.Camera()

        assert bme280 != None
        assert camera != None


class TestInteration():
    def test_instantiation(self):
        motor = interaction.MotorUART()

        assert motor != None


class TestCommunication():
    def test_instantiation(self):
        pass


class TestReasoning():
    def test_instantiation(self):
        policy1 = reasoning.SelectionPolicyByShape()
        policy2 = reasoning.SelectionPolicyByDistance(threshold=10)
        
        assert policy1 != None
        assert policy2 != None
