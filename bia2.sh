#!/bin/bash

cd /root/projects/irso/mysc/mysc
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl bia2
