# -*- coding: utf-8 -*-

from selenium import webdriver


def before_feature(context, feature):
    if 'browser' in feature.tags:
        context.browser = webdriver.Firefox()


def after_feature(context, feature):
    if 'browser' in feature.tags:
        context.browser.quit()
