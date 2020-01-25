#!/bin/bash

./get_articles.py
bundle exec jekyll serve --watch --force_polling
