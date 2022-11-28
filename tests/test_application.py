import pytest
from flask import jsonify
from project.application import application
from datetime import datetime
import logging

logging.basicConfig(filename="output.log",
                    filemode="a",
                    format='%(message)s',
                    level=logging.INFO)

##############################################################################################
#
#   FLASK APP
#
##############################################################################################


@pytest.fixture
def client():
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    f = logging.FileHandler("output.log")
    f.setLevel(logging.INFO)
    f.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(f)
    yield application.test_client()
    logger.removeHandler(f)
    f.close()
    logging.shutdown()


# Multi-Test (Tests 4 inputs at once)
def test_input(client, out=True):
    # Examples of news
    news = {'1':'Donald Trump declares war against aliens',
            '2':'New York best selling author on vacation',
            '3':'Students are spending more time indoors',
            '4':'The weather tomorrow is cloudy with a chance of meatballs'}
    labels = {'1': 1,
              '2': 0,
              '3': 0,
              '4': 1}
    rep = client.get('/', json=news)
    assert rep.status_code == 200
    assert rep.is_json
    assert rep.get_json() is not None
    values = rep.get_json()
    for key in values:
        assert values[key] == labels[key]
    if not out:
        return
    logger.info("Output of Test1: ")
    for key in values:
        logger.info("Test Input: "+news[key])
        logger.info("Expected Response: "+str(labels[key]))
        logger.info("Actual Response: "+str(values[key])+"\n")


# Singleton-Test 1 (Tests 1 input at a time)
def test_fakeinput1(client, out=True):
    # Examples of news
    news = {'1':'End of the world is tomorrow!'}
    labels = {'1': 1}
    rep = client.get('/', json=news)
    assert rep.status_code == 200
    assert rep.is_json
    assert rep.get_json() is not None
    values = rep.get_json()
    for key in values:
        assert values[key] == labels[key]
    if not out:
        return
    logger.info("Output of Test2: ")
    for key in values:
        logger.info("Test Input: "+news[key])
        logger.info("Expected Response: "+str(labels[key]))
        logger.info("Actual Response: "+str(values[key])+"\n\n")


# Singleton-Test 2 (Tests 1 input at a time)
def test_fakeinput2(client, out=True):
    # Examples of news
    news = {'1':'Doctor Oz discovers cure to cancer'}
    labels = {'1': 1}
    rep = client.get('/', json=news)
    assert rep.status_code == 200
    assert rep.is_json
    assert rep.get_json() is not None
    values = rep.get_json()
    for key in values:
        assert values[key] == labels[key]
    if not out:
        return
    logger.info("Output of Test3: ")
    for key in values:
        logger.info("Test Input: "+news[key])
        logger.info("Expected Response: "+str(labels[key]))
        logger.info("Actual Response: "+str(values[key])+"\n\n")


# Singleton-Test 3 (Tests 1 input at a time)
def test_realinput1(client, out=True):
    # Examples of news
    news = {'1':'Expecting clear skies with an average temperature at 21 degrees celsius'}
    labels = {'1': 0}
    rep = client.get('/', json=news)
    assert rep.status_code == 200
    assert rep.is_json
    assert rep.get_json() is not None
    values = rep.get_json()
    for key in values:
        assert values[key] == labels[key]
    if not out:
        return
    logger.info("Output of Test4: ")
    for key in values:
        logger.info("Test Input: "+news[key])
        logger.info("Expected Response: "+str(labels[key]))
        logger.info("Actual Response: "+str(values[key])+"\n\n")


# Singleton-Test 4 (Tests 1 input at a time)
def test_realinput2(client, out=True):
    # Examples of news
    news = {'1':'Schools are expected to reopen in the fall'}
    labels = {'1': 0}
    rep = client.get('/', json=news)
    assert rep.status_code == 200
    assert rep.is_json
    assert rep.get_json() is not None
    values = rep.get_json()
    for key in values:
        assert values[key] == labels[key]
    if not out:
        return
    logger.info("Output of Test5: ")
    for key in values:
        logger.info("Test Input: "+news[key])
        logger.info("Expected Response: "+str(labels[key]))
        logger.info("Actual Response: "+str(values[key])+"\n\n")


# Quality-Test 1 (Calls Test1 100 times and records average response time)
def test_quality_fakeinput1(client):
    time_list = []
    for _ in range(100):
        t1 = datetime.now()
        test_fakeinput1(client, False)
        t2 = datetime.now()
        diff = t2 - t1
        test_time_ms = (diff.seconds * 1000 + diff.microseconds / 1000)
        time_list.append(test_time_ms)
    assert sum(time_list) > 0
    assert len(time_list) == 100
    avg_time_ms = sum(time_list) / len(time_list)
    logger.info("Output of Test6: ")
    logger.info("Test Input: End of the world is tomorrow!")
    logger.info("Expected Response: 1")
    logger.info("Actual Response: 1")
    logger.info("Average Latency Over 100 Calls (ms): "+str(avg_time_ms)+"\n\n")


# Quality-Test 2 (Calls Test2 100 times and records average response time)
def test_quality_fakeinput2(client):
    time_list = []
    for _ in range(100):
        t1 = datetime.now()
        test_fakeinput2(client, False)
        t2 = datetime.now()
        diff = t2 - t1
        test_time_ms = (diff.seconds * 1000 + diff.microseconds / 1000)
        time_list.append(test_time_ms)
    assert sum(time_list) > 0
    assert len(time_list) == 100
    avg_time_ms = sum(time_list) / len(time_list)
    logger.info("Output of Test7: ")
    logger.info("Test Input: Doctor Oz discovers cure to cancer")
    logger.info("Expected Response: 1")
    logger.info("Actual Response: 1")
    logger.info("Average Latency Over 100 Calls (ms): "+str(avg_time_ms)+"\n\n")


# Quality-Test 3 (Calls Test3 100 times and records average response time)
def test_quality_realinput1(client):
    time_list = []
    for _ in range(100):
        t1 = datetime.now()
        test_realinput1(client, False)
        t2 = datetime.now()
        diff = t2 - t1
        test_time_ms = (diff.seconds * 1000 + diff.microseconds / 1000)
        time_list.append(test_time_ms)
    assert sum(time_list) > 0
    assert len(time_list) == 100
    avg_time_ms = sum(time_list) / len(time_list)
    logger.info("Output of Test8: ")
    logger.info("Test Input: Expecting clear skies with an average temperature at 21 degrees celsius")
    logger.info("Expected Response: 0")
    logger.info("Actual Response: 0")
    logger.info("Average Latency Over 100 Calls (ms): "+str(avg_time_ms)+"\n\n")


# Quality-Test 4 (Calls Test4 100 times and records average response time)
def test_quality_realinput2(client):
    time_list = []
    for _ in range(100):
        t1 = datetime.now()
        test_realinput2(client, False)
        t2 = datetime.now()
        diff = t2 - t1
        test_time_ms = (diff.seconds * 1000 + diff.microseconds / 1000)
        time_list.append(test_time_ms)
    assert sum(time_list) > 0
    assert len(time_list) == 100
    avg_time_ms = sum(time_list) / len(time_list)
    logger.info("Output of Test9: ")
    logger.info("Test Input: Schools are expected to reopen in the fall")
    logger.info("Expected Response: 0")
    logger.info("Actual Response: 0")
    logger.info("Average Latency Over 100 Calls (ms): "+str(avg_time_ms))
