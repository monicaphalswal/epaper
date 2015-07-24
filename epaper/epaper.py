#!/usr/bin/env python

import os
from PyPDF2 import PdfFileWriter, PdfFileReader
import urllib2
import shutil
from datetime import date, timedelta
import argparse


codes = {'Jhajjar': "Jhajjar Bhaskar",
        'Delhi': "Delhi Jagran",
        'Haryana':"Dainik Bhaskar Haryana"
       }

urls = {'Jhajjar': "http://digitalimages.bhaskar.com/cph/epaperpdf/%(date)s/%(day)sjhajjar%%20pullout-pg%(page)s-0.pdf", 
        'Delhi': "http://epaper.jagran.com/epaperimages/%(date)s/delhi/%(day)sdel-pg%(page)s-0.pdf",
        'Haryana':"http://digitalimages.bhaskar.com/cph/epaperpdf/%(date)s/%(day)spanipat%%20city-pg%(page)s-0.pdf"
       }
def make_date():
  """
    Create date and day info for url
  """
  today = str(date.today())
  yesterday = date.today() - timedelta(1)
  yesterday = yesterday.day
  if yesterday in range(10):
    yesterdayn = '0'+str(yesterday)
  else:
    yesterdayn = str(yesterday)
  return ''.join(reversed(today.split('-'))), yesterday, yesterdayn

def create_dir(city, day):
  """ 
    Creates a folder on desktop and delete previous day folder
  """
  desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
  directory = desktop + '/' + day +" "+ city 
  if os.path.exists(directory):
    shutil.rmtree(directory)
  day=int(day)+1
  directory = desktop+ '/' + str(day)  + " "+ city 

  if not os.path.exists(directory):
    os.makedirs(directory)
  os.chdir(directory)

def make_pages(start_url, url_date, url_val, city):
  """
    Downloads and  create single pdfs for each page and then combine 
    it into a single pdf
  """
  print("\nDownloading %s paper...\n" % (city))
  page=1
  if os.path.exists("Full-Paper.pdf"):
      print("%s paper has been downloaded already.\n" % (city))
  else:
    continue_loop = True
    output = PdfFileWriter()
    while continue_loop:
      if os.path.exists('Page-' + str(page) + '.pdf'):
        input1 = PdfFileReader(file("Page-"+ str(page)+".pdf", "rb"))
        output.addPage(input1.getPage(0))
        print("Page %s has been downloaded already\n" % (page))
      else:
        url = (start_url) % {'date' :url_date,
                           'day' :url_val,
                           'page' : str(page),
              }  
        print url
        try:
          request = urllib2.urlopen(url)
          print("Downloading %s page number %s \n" % (city, page))
          data = request.read()
          FILE = open('Page-' + str(page) + '.pdf', "wb")
          FILE.write(data)
          FILE.close()
          input1 = PdfFileReader(file("Page-"+ str(page)+".pdf", "rb"))
          output.addPage(input1.getPage(0))
        except urllib2.HTTPError, err:
          if err.code == 404:
            continue_loop = False
      page +=1
    outputStream = file("Full-Paper.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    print("Download for %s completed!!!\n\n" % city)

def download_paper(cities):
  """
    Main function
  """
  date, dayp, day =  make_date()
  for city in cities: 
    create_dir(city, day)
    make_pages(urls[city], date, dayp, city)

def show_available():
  """
    Show list of availble newspapers
  """ 
  print "\n"
  for code in codes:
    print codes[code] + " : " + code
  print "\n"

########################## Execution ##################

def func_main():
  parser = argparse.ArgumentParser(description='Download e-papers and put them in a pdf.')
  parser.add_argument('cities', nargs='*', default=["Jhajjar", "Delhi"],
        help='names of cities (default: Delhi full and Jhajjar pullout)'
      )

  parser.add_argument('-a', '--available', action="store_true",
                     help='names of available newspapers and their codes (name : code)')

  args = parser.parse_args()

  if args.available:
    show_available()
  if not args.available:
    download_paper(args.cities)
