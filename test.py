#coding:utf-8
# test.py
# Copyright (C) 2020 VNR Community（仮）.
# 
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License version 2 as 
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
# 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License version 2 for more details.
# 
#   You should have received a copy of the GNU General Public License
#   version 2 along with this program. If not, see
#   <http://www.gnu.org/licenses/>.
# 

import requests
# TEST
ret = requests.post(url="http://127.0.0.1:5000/callback/requestText", data="試して".encode("utf-8"))
print(ret.text)