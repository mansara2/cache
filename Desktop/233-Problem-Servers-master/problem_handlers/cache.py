#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import base_handler
import math
import random
import json
import logging

from helpers.cache_address_generator import AddressGenerator
from helpers.cache_simulator import CacheSimulator
from helpers import address_sequence

def convert_hex_to_bin(h,space_step):
  """
  Takes a hex sting, and returns a binary string with a space inserted every
  'space_step' bits.
  """
  address_length = 32
  b = bin(int(h[:7],16))[2:].zfill(address_length)
  bl = list(b)
  num_spaces = address_length / space_step
  for i in range(1,num_spaces):
    list_index = (i * space_step) - 1
    bl[list_index] = bl[list_index] + ' '
  return ''.join(bl)

class Cache(base_handler.BaseHandler):
  # Description   - A description of a cache system. (ex: '64KB, 2-way set 
  #                 associative cache with 64byte blocks. The addresses are 40 
  #                 bits)
  # Components    - The components of an address, aka the Tag, Index, and Block
  #                 offset
  # Hit/Miss      - Given a cache description and a set of addresses, which
  #                 addresses are cache hits and which are cache misses
  # Code          - Some random C code loop
  # Address       - Addresses generated by the code loop
  valid_types = [
    "d2c",    # Description to Components
    "hm",     # Address to Hit/Miss
    "c2a"     # Code Loop to Address
  ]
  
  def template_extra_functions(self):
    return [convert_hex_to_bin]

  def maximum_level(self, question_type):
    if question_type == "d2c":
      return 5
    elif question_type == "hm":
      return 2
    else:
      return 31

  def generate_description(self):
    offset = self.generator.randint(4,9)
    index = self.generator.randint(0,10)
    log2_assoc = self.generator.randint(0,4) if index != 0 else self.generator.randint(4,10)
    tag = 32 - (offset+index)
    numsets = 2 ** index
    blocksize = 2 ** offset	
    associativity = 2 ** log2_assoc
    numblocks = numsets * associativity
    cachesize = numblocks * blocksize

    desc_number = (self.level-1) if self.level != 0 else self.generator.randint(1,4)

    assoc_str = 'direct-mapped ' if (associativity == 1) else 'fully-associative ' if (index == 0) else ('' + str(associativity) + '-way set-associative ') 
    size_str = ('' + str(cachesize/1024) + 'KB ') if (cachesize >= 1024) else ('' + str(cachesize) + 'B ')
    set_str = ('' + str(numsets) + ' sets of ') if (index != 0) else ''

    description = [	'Given a cache with ' + str(numsets) + ' sets of blocks of  ' + str(blocksize) + ' bytes, how is the address split up?',
    			'Given a ' + assoc_str + size_str + 'cache with ' + str(blocksize) + ' byte blocks, how is the address split up?',
    			'Given a ' + assoc_str + 'cache consisting of ' + str(numblocks) + ' ' + str(blocksize) + 'B blocks, how is the address split up?',
    			'Given a ' + assoc_str + size_str + 'cache that has ' + str(numblocks) + ' blocks, how is the address split up?',
    			'Given a ' + assoc_str + 'cache with ' + set_str + str(blocksize) + ' byte blocks, how is the address split up?'
		]
    return {"description":description[desc_number], "offset":{"amount":blocksize, "bits":offset}, "index":{"amount":numsets, "bits":index}}
    
  def generate_addresses(self,description):
    """
    Generates 'amount' addresses. Using the cache described by 'description',
    this method will generate types of addresses with given probabilities:
    
    10 percent chance of repeating the same address
    20 percent chance of an unrelated address
    20 percent chance of an address in the same block as an existing address
    20 percent chance of an address in a block adjacent to an existing address
    30 percent chance of an address in the same set as an existing address
    """
    amount = 5 if self.level == 0 else 8
    ag = AddressGenerator(self.generator,description)
    addresses = []
    first = ag.generate_random_address()
    addresses.append(first)
    # Based on how it works out, i is always the index of the previous element
    for i in range(amount-1):
      address_type = self.generator.randint(0,100)
      # 0-10 is same address
      if address_type <= 10:
        logging.warn("Generate Same Address")
        generated = addresses[i]
      # 10-30 is unrelated address
      elif address_type <= 30:
        logging.warn("Generate Random Address")
        generated = ag.generate_random_address()
      else:
        base_address = self.generator.choice(addresses)
        # 30-50 is from the same block
        if address_type <= 50:
          logging.warn("Generate Same Block as %s" % base_address)
          generated = ag.generate_same_block(base_address)
        # 50-70 is from an adjacent block
        elif address_type <= 70:
          logging.warn("Generate Block Adjacent to %s" % base_address)
          generated = ag.generate_adjacent_block(base_address)
        # 70-100 is from the same set
        else:
          logging.warn("Generate Same Set as %s" % base_address)
          generated = ag.generate_same_set(base_address)
      addresses.append(generated)
    return addresses
    
  def indicies_of_hits(self,description,addresses):
    indicies = []
    cache_size = 32768 * description["offset"]["amount"]
    simulator = CacheSimulator(cache_size,description["index"]["amount"],description["offset"]["amount"])
    for i in range(len(addresses)):
      address = int(addresses[i],16)
      hit = simulator.find_block_and_update_lru(address)
      if not hit:
        simulator.fill_cache_with_block(address)
      if hit:
        indicies.append(i)
    return indicies

  def data_for_question(self,question_type):
    if question_type == "d2c":
      return self.generate_description()
    if question_type == "hm":
      description = self.generate_description()
      addresses = self.generate_addresses(description)
      return {"description":description,"addresses":addresses}
    if question_type == "c2a":
      return address_sequence.data_for_question(self.generator, self.level)

  def score_student_answer(self,question_type,question_data,student_answer):
    if question_type == "d2c":
      wanted = self.get_description_string(question_data)
      if wanted == student_answer:
        return (100.0, wanted)
      else:
        return (0.0,wanted)
    if question_type == "hm":
      # Converts the student answer from "1,2,3,4" to [1,2,3,4]
      if student_answer == "":
        student_hits = []
      else:
        student_hits = map(int,student_answer.split(","))
      wanted = self.indicies_of_hits(question_data["description"],question_data["addresses"])
      wanted_set = set(wanted)
      student_set = set(student_hits)
      # This defines an 'incorrect' value as one that shows up in wanted but not
      # student_hits, or shows up in student_hits but not wanted
      num_incorrect = len(wanted_set.difference(student_set).union(student_set.difference(wanted_set)))
      total_addresses = float(len(question_data["addresses"]))
      return (((total_addresses - num_incorrect) / total_addresses) * 100.0,wanted)
    if question_type == "c2a":
      return address_sequence.score_student_answer(question_data, student_answer)

  def get_description_string(self,description):
    offset = description["offset"]["bits"]
    index = description["index"]["bits"]
    tag = 32 - offset - index
    return "%i,%i,%i" % (tag,index,offset)
