# Creates a custom admin command to populate the database from Numbers files exported to csv
from django.core.management.base import BaseCommand, CommandError
from bookkeeping.models import Account, Entry, Distribution

import fileinput
import csv
import datetime

from glob import glob

# List of the columns names in the csv file
COLUMNS = []

# Convert amount extracted as strings from the csv file to floats
def amountToFloat(amountAsString):
    if amountAsString != '':
        return float(amountAsString.replace(",", "."))
    else:
        return -0.0

class Command(BaseCommand):
    help= "Précisez le chemin vers le répertoire où se trouvent les fichiers CSV"

    def add_arguments(self, parser):
        parser.add_argument('path-to-directory', type=str)
    
    def handle(self, **options):
        # Loop through every file in the specified directory for csv files
        for filename in glob(options['path-to-directory'] + '*.csv'):
            with fileinput.FileInput(filename) as f:
                self.stdout.write(f"Examen du fichier {filename}", ending='\n')
                csv_reader = csv.reader(f, delimiter=';')
                csv_to_list = list(csv_reader)
                COLUMNS = csv_to_list[1]
                # Loop through actual entries in the file (starts after the columns'names and stops before totals)
                for line in csv_to_list[2:len(csv_to_list)-1]:
                    # Creates a new income entry
                    if line[0] != '':
                        new_income = Entry(type='INC', label=line[1], amount=amountToFloat(line[2][:-2]), date=datetime.datetime.strptime(line[0], '%d/%m/%Y'))
                        new_income.save()
                    # Creates a new expense entry from the first pieces of data
                    if line[3] != '':
                        new_expense = Entry(type='EXP', label=line[4], amount=amountToFloat(line[5][:-2]), date=datetime.datetime.strptime(line[3], '%d/%m/%Y'))
                        new_expense.save()
                        rank = 6
                        # Creates a new distribution for each registered user in the csv file
                        for amount_column in COLUMNS[6:]:
                            new_distribution_account = Account.objects.get(full_name__contains=COLUMNS[rank])
                            new_distribution = Distribution(entry = new_expense, account=new_distribution_account, amount=amountToFloat(line[rank][:-2]))
                            new_distribution.save()
                            rank += 1
                
        self.stdout.write(self.style.SUCCESS(f'Données importées avec succès !'))
    