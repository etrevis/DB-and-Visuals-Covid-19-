import pdfplumber
import os
import pandas as pd

#
# I apologize for the (very) bad structure, I might move the functions up and organize the code later on
#


#folder for the pdfs
file_folder = os.path.join('Data','PDFs')

#the script works date-by-date and fetches the correct pdfs automaticaly, just set the date here
date = '06/03/2020'

#this is some stuff I will use later for choropleth mapping
reg_list = [[0,'Piemonte'],[1,'Valle d\'Aosta/Vallée d\'Aoste'],[2,'Lombardia'],[3,'Trentino-Alto Adige/Südtirol'],[4,'Veneto'],[5,'Friuli-Venezia Giulia'],[6,'Liguria'],[7,'Emilia-Romagna'],[8,'Toscana'],[9,'Umbria'],[10,'Marche'],[11,'Lazio'],[12,'Abruzzo'],[13,'Molise'],[14,'Campania'],[15,'Puglia'],[16,'Basilicata'],[17,'Calabria'],[18,'Sicilia'],[19,'Sardegna']]
prov_list = [[1, 'Torino'], [2, 'Vercelli'], [3, 'Novara'], [4, 'Cuneo'], [5, 'Asti'], [6, 'Alessandria'], [96, 'Biella'], [103, 'Verbano-Cusio-Ossola'], [7, "Valle d'Aosta/Vallée d'Aoste"], [12, 'Varese'], [13, 'Como'], [14, 'Sondrio'], [15, 'Milano'], [16, 'Bergamo'], [17, 'Brescia'], [18, 'Pavia'], [19, 'Cremona'], [20, 'Mantova'], [97, 'Lecco'], [98, 'Lodi'], [108, 'Monza e della Brianza'], [21, 'Bolzano/Bozen'], [22, 'Trento'], [23, 'Verona'], [24, 'Vicenza'], [25, 'Belluno'], [26, 'Treviso'], [27, 'Venezia'], [28, 'Padova'], [29, 'Rovigo'], [30, 'Udine'], [31, 'Gorizia'], [32, 'Trieste'], [93, 'Pordenone'], [8, 'Imperia'], [9, 'Savona'], [10, 'Genova'], [11, 'La Spezia'], [33, 'Piacenza'], [34, 'Parma'], [35, "Reggio nell'Emilia"], [36, 'Modena'], [37, 'Bologna'], [38, 'Ferrara'], [39, 'Ravenna'], [40, 'Forlì-Cesena'], [99, 'Rimini'], [45, 'Massa-Carrara'], [46, 'Lucca'], [47, 'Pistoia'], [48, 'Firenze'], [49, 'Livorno'], [50, 'Pisa'], [51, 'Arezzo'], [52, 'Siena'], [53, 'Grosseto'], [100, 'Prato'], [54, 'Perugia'], [55, 'Terni'], [41, 'Pesaro e Urbino'], [42, 'Ancona'], [43, 'Macerata'], [44, 'Ascoli Piceno'], [109, 'Fermo'], [56, 'Viterbo'], [57, 'Rieti'], [58, 'Roma'], [59, 'Latina'], [60, 'Frosinone'], [66, "L'Aquila"], [67, 'Teramo'], [68, 'Pescara'], [69, 'Chieti'], [70, 'Campobasso'], [94, 'Isernia'], [61, 'Caserta'], [62, 'Benevento'], [63, 'Napoli'], [64, 'Avellino'], [65, 'Salerno'], [71, 'Foggia'], [72, 'Bari'], [73, 'Taranto'], [74, 'Brindisi'], [75, 'Lecce'], [110, 'Barletta-Andria-Trani'], [76, 'Potenza'], [77, 'Matera'], [78, 'Cosenza'], [79, 'Catanzaro'], [80, 'Reggio di Calabria'], [101, 'Crotone'], [102, 'Vibo Valentia'], [81, 'Trapani'], [82, 'Palermo'], [83, 'Messina'], [84, 'Agrigento'], [85, 'Caltanissetta'], [86, 'Enna'], [87, 'Catania'], [88, 'Ragusa'], [89, 'Siracusa'], [90, 'Sassari'], [91, 'Nuoro'], [92, 'Cagliari'], [95, 'Oristano'], [111, 'Sud Sardegna']]

# regional handling from here
text_re = []
keys = ['hospitalized', 'hospitalized_intensive', 'self_isolation', 'positive' , 'discharged', 'deceased', 'total', 'tested']
keep_line = False
with pdfplumber.open(os.path.join(os.getcwd(), file_folder,"Dati Riepilogo Nazionale "+str(date[1:2])+"marzo2020.pdf")) as pdf:
    for page in pdf.pages:
        for line in page.extract_table(table_settings={"vertical_strategy": "text", "horizontal_strategy": "text"}):
            if 'mbard' in str(line[0]):
                keep_line = True
            if keep_line:
                text_re.append(line)
            if 'OTAL' in str(line[0]):
                break

def int_str(str_):
    if str_ == '' or str_ == None:
        return (int(0))
    else:
        return (int(str_))

def return_rg_list(keys, text_re, reg_list):
    new_list = []
    store_bolzano = []
    for line in text_re:
        new_re = []
        for reg in reg_list:
            #handpicking is always bad, but often necessary
            if 'OTAL' in  line[0]:
                new_re.append(['Italia',pd.NA])
                break
            elif 'omag' in line[0]:
                new_re.append(['Emilia-Romagna',7])
                break
            elif 'olzan' in line[0]:
                store_bolzano = line
                break         
            elif line[0][:5] in reg[1]:
                new_re.append([reg[1],reg[0]])
                break
        for i in range(1,len(keys)+1):
            new_re.append([keys[i-1],int_str(line[i])])
        if len(new_re) == 9:
            new_list.append(new_re)
    #sums Bolzano with Trento 
    for i in range(len(new_list)):
        if new_list[i][0][0]== 'Trentino-Alto Adige/Südtirol':
            true_tren = [['Trentino-Alto Adige/Südtirol',3]]
            for l in range(1,len(keys)+1):
                #print((str(store_bolzano[l])+str(new_list[i][l][1])))
                true_tren.append([new_list[i][l][0],(int_str(store_bolzano[l])+int_str(new_list[i][l][1]))])
            new_list[i] = true_tren
            break
    for line in new_list:
        if len(line) != 9:
            new_list.remove(line)
    return new_list   
# for debug, print all read lines
#for line in text_re:
#    print(line)

li_re = []
for i in range(len(text_re)):
    #Different tables have different formats apparently, this checks for that and deletes extra columns
    line = text_re[i]
    if len(line) == 11:
        del line[2], line[3]
        li_re.append(line)
    elif len(line) == 10:
        del line[2]
        li_re.append(line)

li_re = return_rg_list(keys, text_re, reg_list)

for reg in li_re:
    if int(reg[4][1]) != int(reg[7][1])-int(reg[6][1])-int(reg[5][1]):
        print('ERROR: Total does not match: {}, positive {} is not (total-disch-deces) {}'.format(reg[0][0],reg[4][1],(int(reg[7][1])-int(reg[5][1])-int(reg[6][1]))))


if len(li_re) == 21:
    print('Extracted 21 lines, 20 regions plus Total')
else:
	print('ERROR: Extracted {} lines, expencting 21 regions plus a line for Total'.format(len(li_re)))

def return_reg_df_rows(reg_data, date, prov_list):
    data = {'Date': [], 'Type': [], 'reg_name': [], 'reg_istat_code_num':[],  'prov_name':[],  'prov_istat_code_num':[], 'Value': [] }
    for reg in reg_data:
        for i in range(1, len(reg)):
            if len(reg)==9:
                data['Date'].append(date)
                data['Type'].append(reg[i][0])
                data['reg_name'].append(reg[0][0])
                data['reg_istat_code_num'].append(reg[0][1])
                data['prov_name'].append(pd.NA)
                data['prov_istat_code_num'].append(pd.NA)
                data['Value'].append(reg[i][1])
    return pd.DataFrame(data)    



# Province handling from here, unfortunatly pdfplumber cannot read the tables
text = []
with pdfplumber.open(os.path.join(os.getcwd(),file_folder,"Dati Province "+str(date[1:2])+"marzo2020.pdf")) as pdf:
    for page in pdf.pages:
    	for line in page.extract_text().split('\n'):
    		if ('PCM-DPC'  not in line) and ('Covid 19' not in line) and ('ore ' not in line):
    			text.append(line.capitalize())

li_ = []
re = []
for line in text:	
	for reg in reg_list:
		if line[:5] in reg[1] and len(re)==0:
			re.append([reg[1],reg[0]])
	if 'Totale' not in line and (line[:6] not in re[0][0]):
		#print(line)
		re.append(line)
	elif 'verifi' in line or 'ggior' in line:
		re.append(line)
	elif 'Totale' in line:
		li_.append(re)
		re = []

count = 0
for rg in li_:
	for i in range(1,len(rg)):
		if not 'ggior' in rg[i] and 'verifi' not in rg[i]:
			rg[i] = rg[i].split(' ')
		elif 'ggior' in rg[i] or 'verifi' in rg[i]:
			temp = rg[i].split(' ')
			count +=1
			try:
				rg[i] = ['Testing',int(temp[len(temp)-1])]
			except:
				rg[i] = ['Testing',0]
		if len(rg[i])>2:
			if 'Reggio' in rg[i][0]:
				if 'Emilia' in rg[0][0]:
					rg[i] = ["Reggio nell'Emilia",rg[i][len(rg[i])-1]]
				elif 'calabria' in rg[0][0]:
					rg[i] = ["Reggio di Calabria",rg[i][len(rg[i])-1]]
			elif 'spe' in rg[i][1]:
				rg[i] = ["La Spezia",rg[i][len(rg[i])-1]]
			elif 'Massa' in rg[i][0]:
				rg[i] = ["Massa-Carrara",rg[i][len(rg[i])-1]]
			elif 'cese' in rg[i][1]:
				rg[i] = ["Forlì-Cesena",rg[i][len(rg[i])-1]]
			elif 'Monza' in rg[i][0]:
				rg[i] = ["Monza e della Brianza",rg[i][len(rg[i])-1]]
			else:
				rg[i] = [rg[i][0],rg[i][len(rg[i])-1]]

print('Expecting {} unmatched (Testing):'.format(count))
for rg in li_:
	for i in range(1,len(rg)):
		total = 1
		for prov in prov_list:
			if rg[i][0][:8] in prov[1]:
				cont = False
				total += -1
				if not rg[i][0]==prov[1]:
					rg[i][0]==prov[1]
			elif "L'aqui" in  rg[i][0]:
				rg[i][0] = "L'aquila"
				total += -1
			elif 'Bat'==rg[i][0]:
				rg[i] = ['Barletta-Andria-Trani',rg[i][len(rg[i])-1]]
				total += -1
			elif 'Verbano' in rg[i][0]:
				rg[i] = ['Verbano-Cusio-Ossola',rg[i][len(rg[i])-1]]
				total += -1
			elif 'Pesaro'==rg[i][0]:
				rg[i] = ['Pesaro e Urbino',rg[i][len(rg[i])-1]]
				total += -1
		if total == 1:
			print('Found unmatched: {}={} in {}'.format(rg[i][0],rg[i][1], rg[0][0]))

if total > 0:
	print("Check the unmatched, only 'Testing' are expected")

li_.remove([])

def return_prov_df_rows(prov_data, date, prov_list):
	data = {'Date': [], 'Type': [], 'reg_name': [], 'reg_istat_code_num':[],  'prov_name':[],  'prov_istat_code_num':[], 'Value': [] }
	for reg in prov_data:
		for i in range(1, len(reg)):
			for prov in prov_list:
				if reg[i][0][:8] in prov[1] and len(reg[i])==2:
					data['Date'].append(date)
					data['Type'].append('total_p')
					data['reg_name'].append(reg[0][0])
					data['reg_istat_code_num'].append(reg[0][1])
					data['prov_name'].append(prov[1])
					data['prov_istat_code_num'].append(prov[0])
					data['Value'].append(reg[i][1])
					break
				elif 'Testing' == reg[i][0] and len(reg[i])==2:
					data['Date'].append(date)
					data['Type'].append('testing')
					data['reg_name'].append(reg[0][0])
					data['reg_istat_code_num'].append(reg[0][1])
					data['prov_name'].append(pd.NA)
					data['prov_istat_code_num'].append(pd.NA)
					data['Value'].append(reg[i][1])
					break
	return pd.DataFrame(data)


df = pd.read_csv(os.path.join(os.getcwd(),'Data','DB.csv'), sep=',', header=0)

new_df = df.append(return_prov_df_rows(li_, date, prov_list), ignore_index=True)
new_df_2 = new_df.append(return_reg_df_rows(li_re, date, prov_list), ignore_index=True)

new_df_2.to_csv(os.path.join(os.getcwd(),'Data','DB.csv'), sep=',', index=False)