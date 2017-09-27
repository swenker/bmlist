#!/bin/env bash

function update_prod_settings(){
    sed -i 's/DEBUG = True/DEBUG = False/' ../iamtest.py
    sed -i 's/centos.blurdev.com/localhost/' ../iamtest.py
    sed -i 's;/var/www/html/static;/var/bmlist/www/html/static;' ../iamtest.py
}

update_prod_settings