#!/usr/bin/python

from subprocess import call 

def build_report():
   args = ("reportPDF","http://127.0.0.1:5000/http_apps")
   LINK = "http://localhost:5000/"
   call(["/usr/local/bin/wkhtmltopdf",LINK+"report_apps","report/all_apps.pdf"])
   call(["/usr/local/bin/wkhtmltopdf",LINK+"http_apps","report/http_apps.pdf"])
   call(["/usr/local/bin/wkhtmltopdf",LINK+"app_groups","report/app_groups.pdf"])
   call(["/usr/local/bin/wkhtmltopdf",LINK+"app_bar","report/app_bar.pdf"])
   call(["/usr/local/bin/wkhtmltopdf",LINK+"app_pie","report/app_pie.pdf"])
   call(["/usr/local/bin/wkhtmltopdf",LINK+"app_bubble","report/app_bubble.pdf"])
   call(["/usr/local/bin/wkhtmltopdf",LINK+"char_bar","report/char_bar.pdf"])
   call(["/usr/local/bin/wkhtmltopdf",LINK+"char_pie","report/char_pie.pdf"])
   call(["/usr/local/bin/wkhtmltopdf",LINK+"category_bar","report/category_bar.pdf"])
   call(["/usr/local/bin/wkhtmltopdf",LINK+"category_pie","report/category_pie.pdf"])
   call(["/usr/local/bin/wkhtmltopdf",LINK+"subcategory_bar","report/subcategory_bar.pdf"])
   call(["/usr/local/bin/wkhtmltopdf",LINK+"subcategory_pie","report/subcategory_pie.pdf"])
 
if __name__ == '__main__':
   build_report()


