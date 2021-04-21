'''
this file is created to work with data in /home/zz/Cloud/GDrive/ziqizhang/project/innovateuk-Vamstar/Link to Vamstar Data/google/extracted documents - manual/drive-download-20210324T213237Z-001
or https://drive.google.com/drive/folders/1_qzCYkfHS8s5E43HiE5FBEAZpY2PLbx-?usp=sharing

it loads the folders, check against a master spreadsheet file, to find out the
- country
- buyer

then rearrange the folder into a hierarchy of country > buyer
'''

import pandas as pd
import os,shutil,sys,urllib.parse


#/home/zz/Cloud/GDrive/ziqizhang/project/innovateuk-Vamstar/Link to Vamstar Data/google/extracted documents - manual/drive-download-20210324T213237Z-001
def rearrange(inCSV, inFolder, outFolder):
    df = pd.read_csv(inCSV, header=0, delimiter=',', quoting=0, encoding="utf-8",
                     ).fillna("none")

    vamid2country={}
    vamid2buyer={}

    country2buyers={}
    buyer2samples={}

    filter=set()
    for f in os.listdir(inFolder):
        filter.add(f)

    for index, row in df.iterrows():
        vamid = row["vam_id"]
        # if vamid=="DY_a9nqLX7KWxK4ntF7jWqYIruck7yiTJVI6l8plYaA":
        #     print()
        country = row["entity_iso_country"]
        buyer = row["buyer_main_url"]
        if "venetostrade.it" in buyer:
            print()
        parsed_url = urllib.parse.urlparse(buyer)
        host = parsed_url.path
        if host=="" or len(host)<2:
            host=parsed_url.netloc

        vamid2buyer[vamid]=host
        vamid2country[vamid]=country

        if vamid in filter:
            if country in country2buyers.keys():
                cbuyers=country2buyers[country]
            else:
                cbuyers=set()
            cbuyers.add(buyer)
            country2buyers[country]=cbuyers

            if buyer in buyer2samples:
                count = buyer2samples[buyer]
            else:
                count=0
            count+=1
            buyer2samples[buyer]=count


    for f in os.listdir(inFolder):
        if f not in vamid2country.keys() or f not in vamid2buyer.keys():
            print("error: this id does not match to any entry:"+f)
            continue

        country=vamid2country[f]
        buyer = vamid2buyer[f]

        newfolder=outFolder+"/"+country+"/"+buyer+"/"+f

        shutil.move(inFolder+"/"+f, newfolder)

    for k,v in country2buyers.items():
        line=""
        for b in v:
            bc = buyer2samples[b]
            line+=" "+b+" ("+str(bc)+"),"

        print(k+"\t"+line)




if __name__ == "__main__":
    #extract_english_2kbiocon(sys.argv[1], sys.argv[2])

    rearrange(sys.argv[1], sys.argv[2], sys.argv[3])

