import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import streamlit as st

from PIL import Image
import timeit
from io import BytesIO


custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style = "ticks", rc = custom_params)
######################################################################

### Função para ler os arquivos

@st.cache_data

def load_data(file_data):
	try:
		return pd.read_csv(file_data, sep = ";")
	except:
		return pd.read_excel(file_data)
######################################################################

### Selecionando All

@st.cache_data

def multiselect_filter(relatorio, col, selecionados):
	if "all" in selecionados or not selecionados:
		return relatorio
	else:
		return relatorio[relatorio[col].isin(selecionados)].reset_index(drop = True)
########################################################################

### Expotando os arquivos

@st.cache_data
def convert_df(df):
	return df.to_csv(index = False).encode('utf-8')

@st.cache_data
def to_excel(df):
	output = BytesIO()
	writer = pd.ExcelWriter(output, engine='xlsxwriter')
	df.to_excel(writer, index = False, sheet_name = "sheet1")
	writer.close()
	processed_data  = output.getvalue()
	return processed_data
########################################################################

### App principal

def main():
	st.set_page_config(page_title = "Telemarketing Analisys",
		page_icon = Image.open(r"D:\Documentos\Profissional\Cursos\EBAC\Dados\Desenvolvimento\EBAC_Modulo28\telmarketing_icon.png"),
		layout = "wide",
		initial_sidebar_state = 'expanded')

	image = Image.open(r"D:\Documentos\Profissional\Cursos\EBAC\Dados\Desenvolvimento\EBAC_Modulo28\Bank-Branding.jpg")
	st.image(image, )
	st.write("# Telemarketing Analisys ☎️")
	st.markdown("---")

	st.sidebar.write("## Faça upload do arquivo")
	data_file_1 = st.sidebar.file_uploader("Bank Marketing Data", type = ['csv', 'xlsx'])


	if data_file_1 is not None:
		st.sidebar.write(f"Arquivo carregado: {data_file_1.name}")

		start = timeit.default_timer()
		bank_raw = load_data(data_file_1)
		bank = bank_raw.copy()
		load_time = timeit.default_timer() - start

		st.write("## Dataframe sem a aplicação do filtro 📎")
		st.write(bank_raw.head()) 

		st.write("Tempo: ", load_time, "segundos")
		
######################################################
		st.sidebar.write("## Valores Aplicados nos Filtros 📌")	
### Filtros

		with st.popover("Filtros 📌"):
			with st.form(key="filters_form"):

### Idades
				max_age = int(bank.age.max())
				min_age = int(bank.age.min())

				idades = st.slider(label = "Idade", 
					min_value = min_age, 
					max_value = max_age, 
					value = (min_age, max_age),
					step = 1)
				st.sidebar.write('Idades 🎂:', idades)
	#################################################
	## Profissões
				jobs_list = bank.job.unique().tolist()
				jobs_list.append("all")		
				jobs_list = sorted(jobs_list)	
				jobs_selected = st.multiselect("Profissão", jobs_list, ["all"])
				st.sidebar.write('Profissões ⚒️:', jobs_selected)
	#################################################
	## Estado Civil
				civil_list = bank.marital.unique().tolist()
				civil_list.append("all")
				civil_list = sorted(civil_list)	
				civil_selected = st.multiselect("Estado Civil", civil_list, ["all"])	
				st.sidebar.write('Estado Civil 👰:', civil_selected)
		
	#################################################
	## Default?
				def_list = bank.default.unique().tolist()
				def_list.append("all")
				def_list = sorted(def_list)	
				def_selected = st.multiselect("Default", def_list, ["all"])
				st.sidebar.write('Default:', def_selected)
	#################################################
	## Financiamento?
				fin_list = bank.housing.unique().tolist()
				fin_list.append("all")
				fin_list = sorted(fin_list)	
				fin_selected = st.multiselect("Tem Financiamento Imobiliário?", fin_list, ["all"])
				st.sidebar.write('Tem Financiamento Imobiliário? 🏠', fin_selected)
	#################################################
	## Emprestimo?
				emp_list = bank.loan.unique().tolist()
				emp_list.append("all")
				emp_list = sorted(emp_list)	
				emp_selected = st.multiselect("Tem empréstimo?", emp_list, ["all"])
				st.sidebar.write('Tem emprestimo?', emp_selected)
	#################################################
	## Contato
				cont_list = bank.contact.unique().tolist()
				cont_list.append("all")
				cont_list = sorted(cont_list)	
				cont_selected = st.multiselect("Meio de Contato", cont_list, ["all"])
				st.sidebar.write('Meio de Contato 📳:', cont_selected)
	#################################################
	## Mês
				mes_list = bank.month.unique().tolist()
				mes_list.append("all")
				jmes_list = sorted(mes_list)	
				mes_selected = st.multiselect("Mês de Contato", mes_list, ["all"])
				st.sidebar.write('Mês de Contato 📅:', mes_selected)	
	#################################################
	## Dia da Semana
				dia_list = bank.day_of_week.unique().tolist()
				dia_list.append("all")
				dia_list = sorted(dia_list)	
				dia_selected = st.multiselect("Dia da Semana do Contato", dia_list, ["all"])
				st.sidebar.write('Dia da Semana do Contato 📅:', dia_selected)
				submit_button = st.form_submit_button(label="Aplicar")

###############################################################

## Dataframe com filtro

		bank = (bank.query("age >= @idades[0] and age <= @idades[1]")
			.pipe(multiselect_filter, 'job', jobs_selected)
			.pipe(multiselect_filter, 'marital', civil_selected)
			.pipe(multiselect_filter, 'default', def_selected)
			.pipe(multiselect_filter, 'housing', fin_selected)
			.pipe(multiselect_filter, 'loan', emp_selected)
			.pipe(multiselect_filter, 'contact', cont_selected)
			.pipe(multiselect_filter, 'month', mes_selected)
			.pipe(multiselect_filter, 'day_of_week', dia_selected)	
		)

		st.write("## Dataframe com a aplicação do filtro 🖇️")
		st.write(bank.head()) 
################################################################

### Botões de download dos dados filtrados

		df_xlsx = to_excel(bank)
		st.download_button (label = "Download do Dataframe Filtrado em .xlsx 📥", data = df_xlsx, file_name = 'data_filtred.xlsx')
################################################################

		bank_raw_target_perc = bank_raw['y'].value_counts(normalize = True)*100
		bank_raw_target_perc = bank_raw_target_perc.sort_index()	

		try: 
			bank_target_perc = bank.y.value_counts(normalize = True)*100
			bank_target_perc = bank_target_perc.sort_index()
		
		except:
			st.error("Erro no filtro")

		st.write("## Proporção de Aceite 📊")

### Selecionando o tipo de gráfico

		col1, col2 = st.columns([1,3])  

		with col1:
                	graf = st.radio("Tipo de Gráfico:", ["Barras", "Pizza"], key="graph_type", 
                                horizontal=True, 
                                label_visibility="visible"
                                )
		with col2:
			st.write("")
		
		fig, ax = plt.subplots(1, 2, figsize = (10, 3)) 

		if graf == "Barras":
### Plotagem sem filtro
			sns.barplot(x = bank_raw_target_perc.index, 
				y = bank_raw_target_perc.values,
				ax = ax[0])
			ax[0].bar_label(ax[0].containers[0])
			ax[0].set_title("Dados não filtrados", fontweight = "bold")

### Plotagem com filtro
			sns.barplot(x = bank_target_perc.index, 
				y = bank_target_perc.values,
				ax = ax[1])
			ax[1].bar_label(ax[1].containers[0])
			ax[1].set_title("Dados filtrados", fontweight = "bold")
		
		else:
### Plotagem sem filtro
			bank_raw_target_perc.plot(kind = 'pie', autopct = '%.2f', y = 'y', ax = ax[0])
			ax[0].set_title("Dados não filtrados", fontweight = "bold")
			ax[0].set_ylabel("")

### Plotagem com filtro
			bank_target_perc.plot(kind = 'pie', autopct = '%.2f', y = 'y', ax = ax[1])
			ax[1].set_title("Dados filtrados", fontweight = "bold")
			ax[1].set_ylabel("")
		
		st.pyplot(fig)


		col1, col2 = st.columns(2)  

		df_xlsx = to_excel(bank_raw_target_perc)
		col1.write('### Proporção sem filtro')
		col1.write(bank_raw_target_perc)
		col1.download_button(label='📥 Download',
                            	data=df_xlsx ,
                            	file_name= 'bank_raw_y.xlsx')
        
		df_xlsx = to_excel(bank_target_perc)
		col2.write('### Proporção com filtros')
		col2.write(bank_target_perc)
		col2.download_button(label='📥 Download',
                            	data=df_xlsx ,
                            	file_name= 'bank_y.xlsx')


if __name__ == "__main__":
	main()
