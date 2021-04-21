
import pandas as pd
import sys, csv
import urllib.parse

#file: /home/zz/Cloud/GDrive/ziqizhang/project/innovateuk-Vamstar/Link to Vamstar Data/google/f02_data_2k_biocon.xlsx
#method to process the f02_data_2k_biocon.xlsx file and output a filtered version containing english entries only
def extract_english_2kbiocon(in_csv, out_csv):
    col_lang = "entity_original_language"
    col_notice_url="notice_url"
    col_buyer_name="buyer_name_english_derived"
    col_buyer_communication_url_doc="buyer_communication_url_docs"
    col_lot_title="lot_title"
    col_lot_procurement_description="lot_procurement_description"
    col_lot_active_ingredient_orig_en="lot_active_ingredient_orig_en"
    col_active_ingredient_orig_en="active_ingredient_orig_en"

    f= open(out_csv, 'w', newline='\n')
    csv_writer = csv.writer(f, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
    csv_writer.writerow([col_active_ingredient_orig_en,
                         col_lang,
                         col_notice_url,
                         col_buyer_name,
                         col_buyer_communication_url_doc,
                         col_lot_title,
                         col_lot_procurement_description,
                         col_lot_active_ingredient_orig_en])

    df = pd.read_csv(in_csv, header=0, delimiter=',', quoting=0, encoding="utf-8",
                       ).fillna("none")

    for index, row in df.iterrows():
        lang = row[col_lang]
        if lang.lower()!="en":
            continue
        newr = [row[col_active_ingredient_orig_en],
                row[col_lang],
                row[col_notice_url],
                row[col_buyer_name],
                row[col_buyer_communication_url_doc],
                row[col_lot_title],
                row[col_lot_procurement_description],
                row[col_lot_active_ingredient_orig_en],
                ]
        csv_writer.writerow(newr)

    f.close()

#file: /home/zz/Cloud/GDrive/ziqizhang/project/innovateuk-Vamstar/Link to Vamstar Data/google/f02_data_2k_biocon.xlsx
#method to process the f02_data_2k_biocon.xlsx file and output a filtered version containing entries with useful
#buyer communication doc, from ANY language
#'useful' as: long url
def extract_bcd_2kbiocon(in_csv, out_csv):
    col_country="entity_iso_country"
    col_lang = "entity_original_language"
    col_notice_url="notice_url"
    col_buyer_name="buyer_name_english_derived"
    col_buyer_communication_url_doc="buyer_communication_url_docs"
    col_lot_title="lot_title"
    col_lot_procurement_description="lot_procurement_description"
    col_lot_active_ingredient_orig_en="lot_active_ingredient_orig_en"
    col_active_ingredient_orig_en="active_ingredient_orig_en"

    f= open(out_csv, 'w', newline='\n')
    csv_writer = csv.writer(f, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
    csv_writer.writerow([col_active_ingredient_orig_en,
                         col_lang,
                         col_country,
                         col_notice_url,
                         col_buyer_name,
                         col_buyer_communication_url_doc,
                         col_lot_title,
                         col_lot_procurement_description,
                         col_lot_active_ingredient_orig_en])

    df = pd.read_csv(in_csv, header=0, delimiter=',', quoting=0, encoding="utf-8",
                       ).fillna("none")


    buyer_and_tender={}
    country_and_tender={}
    country_and_buyers = {}
    country_and_sources = {}
    for index, row in df.iterrows():
        bcd = row[col_buyer_communication_url_doc].strip()
        if len(bcd)<50:
            continue
        buyer=row[col_buyer_name]
        tender=row[col_notice_url]
        country=row[col_country]
        bcd_url=row[col_buyer_communication_url_doc]
        parsed_url = urllib.parse.urlparse(bcd_url)
        host=parsed_url.netloc

        if buyer in buyer_and_tender.keys():
            tenders = buyer_and_tender[buyer]
            tenders.add(tender)
        else:
            tenders = set()
            tenders.add(tender)
            buyer_and_tender[buyer]=tenders

        if country in country_and_tender.keys():
            tenders = country_and_tender[country]
            tenders.add(tender)
        else:
            tenders = set()
            tenders.add(tender)
            country_and_tender[country]=tenders

        if country in country_and_buyers.keys():
            buyers = country_and_buyers[country]
            buyers.add(buyer)
        else:
            buyers = set()
            buyers.add(buyer)
            country_and_buyers[country]=buyers

        if country in country_and_sources.keys():
            sources = country_and_sources[country]
            sources.add(host)
        else:
            sources = set()
            sources.add(host)
            country_and_sources[country]=sources


        newr = [row[col_active_ingredient_orig_en],
                row[col_lang],
                country,
                tender,
                buyer,
                row[col_buyer_communication_url_doc],
                row[col_lot_title],
                row[col_lot_procurement_description],
                row[col_lot_active_ingredient_orig_en],
                ]
        csv_writer.writerow(newr)

    print("BUYER AND TENDERS>>>")
    buyers = sorted(list(buyer_and_tender.keys()))
    for b in buyers:
        print("{}={}".format(b, len(buyer_and_tender[b])))

    print("\nCOUNTRY AND TENDERS>>>")
    countries = sorted(list(country_and_tender.keys()))
    for c in countries:
        print("{}={}".format(c, len(country_and_tender[c])))

    print("\nCOUNTRY AND BUYERS>>>")
    countries = sorted(list(country_and_buyers.keys()))
    for c in countries:
        print("{}={}".format(c, len(country_and_buyers[c])))

    print("\nCOUNTRY AND TENDER SOURCES>>>")
    countries = sorted(list(country_and_sources.keys()))
    for c in countries:
        print("{}={}".format(c, country_and_sources[c]))

    f.close()

#method that reads back 'f02_data_2k_biocon_filtered_bcd-v1.xlsx' (created by extract_bcd_2kbiocon),
#check how many source websites requires downloads and print these.
def check_sources():
    pass

if __name__ == "__main__":
    #extract_english_2kbiocon(sys.argv[1], sys.argv[2])

    extract_bcd_2kbiocon(sys.argv[1], sys.argv[2])