# -*- coding: utf-8 -*-

from selenium import webdriver
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "myfinance.settings"


def before_feature(context, feature):
    if 'browser' in feature.tags:
        context.browser = webdriver.Firefox()


def after_feature(context, feature):
    if 'browser' in feature.tags:
        context.browser.quit()
