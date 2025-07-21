import streamlit as st

def markdown_string() -> str:
    return """<style>
                /* 1) Descendant selector: find the nested <input> */
                div[data-baseweb="input"] {
                    border: none !important;
                    box-shadow: none !important;
                    background: transparent !important;
                }
                div[data-baseweb="base-input"] {
                    border: none !important;
                    box-shadow: none !important;
                    background: transparent !important;
                }
                div[data-baseweb="input"] input:focus,
                div[data-baseweb="input"] textarea:focus {
                    outline: none !important;
                }
                div[data-baseweb="input"] textarea {
                    background-color: #0f1116 !important;
                    border: none !important;          
                    border-radius: 6px     !important;
                    padding: 8px 12px      !important;
                    color: #fff            !important; 
                    box-shadow: none !important; 
                }

                /* 2) Focus state */
                div[data-baseweb="input"] input:focus,
                div[data-baseweb="input"] textarea:focus {
                    box-shadow: 0 0 0 0px rgba(251, 8, 255, 0.3) !important;
                    border-color: none !important;
                }

                /* 4) Now override just the Search JSON box */
                div[data-baseweb="input"] input[aria-label="Search Parsed Data"] {
                    background-color: #262730 !important;  
                    color: #fff !important;              
                    border-radius: 6px !important;       
                    padding: 8px 12px !important;
                }
                div[data-baseweb="input"] input[aria-label="Search Parsed Data"]:focus {
                    outline: none !important;
                    /* you could add a focus glow here if you like */
                }
                </style>
            """
