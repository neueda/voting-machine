#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json
import unittest

import Voting

class VotingIT(unittest.TestCase):
  def testVote1(self):
    Voting.vote(1)

    webhandle = urllib2.urlopen('http://dmi3.net/plusminus/?pulse')
    votes=json.loads(webhandle.read())
    latest_vote=votes[0]
    
    self.assertEqual(latest_vote['action'],'rigadevday')
    self.assertEqual(latest_vote['amount'],1)

  def testVote0(self):
      Voting.vote(0)

      webhandle = urllib2.urlopen('http://dmi3.net/plusminus/?pulse')
      votes=json.loads(webhandle.read())
      latest_vote=votes[0]
      
      self.assertEqual(latest_vote['action'],'rigadevday')
      self.assertEqual(latest_vote['amount'],0)
  

if __name__ == '__main__':
  unittest.main()

