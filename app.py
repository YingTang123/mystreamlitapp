import tensorflow as tf  
from tensorflow.keras.models import load_model
import streamlit as st
import numpy as np
import os

path = os.getcwd().replace("\\", "/")

st.set_page_config(
    page_title="Python deep model",
    page_icon="",
    layout="wide"
)

if os.path.exists(path+"/model01.h5") and os.path.exists(path+"/model01.h5"):
    pass
else:
    from filesplit.merge import Merge

    merge = Merge(inputdir = path+"/model1", outputdir=path, outputfilename = "model01.h5")
    merge.merge()
    merge = Merge(inputdir = path+"/model2", outputdir=path, outputfilename = "model02.h5")
    merge.merge()

with st.sidebar:
    st.markdown('''
        <h1 style="text-align: center; font-size: 20px; color: white; background: #ff4b4b; border-radius: .5rem; margin-bottom: 1rem; padding: 1rem;">
            Deep learning-based models for predicting PC-AKI in CKD patients undergoing coronary angiography and intervention
        </h1>
    ''', unsafe_allow_html=True)
    
    m = st.radio(
        "**Please select model:**",
        ["**model1**", "**model2**"],
        index=0,
    )
    
    t = "This predictive models can be used to predict the risk of PC-AKI after coronary angiography and intervention in adult patients with CKD (eGFR ＜ 60 ml/min/1.73m²), aiding in risk stratification and guiding management recommendations. Model 1 includes preoperative variables for preoperative assessment, whereas Model 2 includes additional intraoperative variables for postoperative assessment."
    
    st.markdown(f'''
        <div style="font-size: 20px; color: black; background: none; border: 1px solid #ff4b4b; border-radius: .5rem; margin-bottom: 5px; padding: 1rem;">
            <div style="text-align: center; border-bottom: 1px solid gray;">About</div>
            <p style="font-size: 16px; text-align:left;">{t}</p>
        </div>
    ''', unsafe_allow_html=True)

st.markdown('''
    <style>
        [data-testid="stRadio"] {
            border: 1px solid #ff4b4b; 
            border-radius: .5rem;
            padding: 1rem;
        }
    </style>''', unsafe_allow_html=True)

x1 = {"Yes":1, "No":0}
x2 = {i:j for j, i in enumerate(["-/+-","+","2+","3+","4+"])}

d1 = {
    "Urine protein":None,
    "Diuretic":None,
    "MI":None,
    "Diabetes":None,
    "CHF":None,
    "TNT":None,
    "β-blocker":None,
    "NTpro-BNP":None,
    "Hemoglobin":None,
    "CK":None,
    "Arrhythmia":None,
    "LVEF":None,
    "CK-MB":None,
    "Albumin":None,
    "Ca2+":None,
    "Vasoactive agent":None,
    "IABP":None,
    "Contrast volumes":None,
    "PCI":None,
    "Emergency procedure":None
}

with st.form("Model input parameters"):
    st.markdown(f'''
        <div style="text-align: center; font-size: 20px; color: white; background: #ff4b4b; border-radius: .5rem; margin-bottom: 1rem; padding: 1rem;">
            Model input parameters (Current model is '{m.strip("*")}')
        </div>
    ''', unsafe_allow_html=True)
    
    if m!="**model1**":
        col = st.columns(4)
    else:
        col = st.columns(3)
    
    d1["Urine protein"] = x2[col[0].selectbox("Urine protein", ["-/+-","+","2+","3+","4+"])]
    d1["Diuretic"] = x1[col[0].selectbox("Diuretics", ["Yes","No"])]
    d1["MI"] = x1[col[0].selectbox("Myocardial infarction", ["Yes","No"])]
    d1["Diabetes"] = x1[col[0].selectbox("Diabetes", ["Yes","No"])]
    d1["CHF"] = x1[col[0].selectbox("Congestive heart failure", ["Yes","No"])]
    d1["TNT"] = col[1].number_input("Cardiac troponin T(pg/ml)")
    d1["β-blocker"] = x1[col[1].selectbox("β-blockers", ["Yes","No"])]
    d1["NTpro-BNP"] = col[1].number_input("NTpro-BNP(pg/ml)")
    d1["Hemoglobin"] = col[1].number_input("Hemoglobin(g/l)")
    d1["CK"] = col[1].number_input("Creatine Kinase(U/l)")
    d1["Arrhythmia"] = x1[col[2].selectbox("Arrhythmia", ["Yes","No"])]
    d1["LVEF"] = col[2].number_input("Left ventricular ejection fraction(%)")
    d1["CK-MB"] = col[2].number_input("Creatine kinase-MB(U/l)")
    d1["Albumin"] = col[2].number_input("Albumin(g/l)")
    d1["Ca2+"] = col[2].number_input("Calcium(mmol/l)")
    
    if m!="**model1**":
        d1["Vasoactive agent"] = x1[col[3].selectbox("Vasoactive drugs", ["Yes","No"])]
        d1["IABP"] = x1[col[3].selectbox("Intra-aortic balloon pump", ["Yes","No"])]
        d1["Contrast volumes"] = col[3].number_input("Volumes of iodinated contrast media(ml)")
        d1["PCI"] = x1[col[3].selectbox("Percutaneous coronary intervention", ["Yes","No"])]
        d1["Emergency procedure"] = x1[col[3].selectbox("Emergency procedure", ["Yes","No"])]
    else:
        pass
    
    submitted = st.form_submit_button("Start predict", use_container_width=True)

if submitted:
    if m=="**model1**":
        model = load_model(path+'/model01.h5', compile=True)
        res = model.predict(np.array([list(d1.values())[:-5]]))

        if res<0.456:
            st.info("""
                **This patient is considered to be at low risk for PC-AKI.**    
                **Recommendations: Administer preoperative hydration as needed, monitor renal function, and use low- or iso-osmolar contrast media.**
            """)
        else:
            st.info("""
                **This patient is considered to be at high risk for PC-AKI.**    
                **Recommendations: Administer preoperative hydration, closely monitor renal function, use low- or iso-osmolar media, limit the volume of contrast media, and minimize the use of nephrotoxic drugs.**
            """)

    if m=="**model2**":
        model = load_model(path+'/model02.h5', compile=True)
        res = model.predict(np.array([list(d1.values())]))

        if res<0.456:
            st.info("""
                **This patient is considered to be at low risk for PC-AKI.**    
                **Recommendations: Administer postoperative hydration as needed and monitor renal function.**
            """)
        else:
            st.info("""
                **This patient is considered to be at high risk for PC-AKI.**    
                **Recommendations: Administer postoperative hydration, closely monitor renal function and internal environment status, avoid multiple contrast media injections within 72 hours, minimize the use of nephrotoxic drugs, request for nephrology consultation, arrange for more frequent follow-up.**
            """)
