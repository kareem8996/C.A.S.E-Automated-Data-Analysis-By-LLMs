import streamlit as st
from streamlit_cookies_controller import CookieController
import os
import pandas as pd
import requests
class MultiPageApp():
    """
    A class to create a multi-page Streamlit application.
    
    Attributes
    ----------
    pages : list
        A list to store the pages of the application.
    
    Methods
    -------
    add_page(directory, title, default=False)
        Adds a new page to the application.
    
    run()
        Runs the Streamlit application with the configured pages and layout.
    """
    def __init__(self,controller) -> None:
        self.pages=[]
        self.auth_pages={}
        self.controller=controller
        # st.session_state['cookie_man']=True
        

        if 'loggedIn' not in st.session_state:
            st.session_state['loggedIn']=False


        if 'signUp_Page' not in st.session_state:
            st.session_state['signUp_Page']=False
        
        st.markdown("""
                    <style>
                    [data-testid="stLogo"] {
                        width: 350px;  /* Adjust width as needed */
                        height: auto;  /* Maintain aspect ratio */
                    }
                    </style>

                """, unsafe_allow_html=True) 

    def add_page(self,directory,title,default=False):
        """
        Adds a new page to the application.
        
        Parameters
        ----------
        directory : str
            The directory path of the page script.
        title : str
            The title of the page.
        default : bool, optional
            Indicates if this page is the default page (default is False).
        
        Returns
        -------
        None
        """
        self.pages.append(st.Page(directory,title=title,default=default))
        
    def login(self):
        st.session_state['loggedIn']=False
        pg=st.navigation(self.pages[:3])
        pg.run()

    def logout(self):
        st.empty()
        st.session_state['loggedIn'] = False
        self.controller.remove(f"user_{st.session_state['user_id']}_session")        


    def run(self):
        """
        Runs the Streamlit application with the configured pages and layout.
        
        Sets up the page configuration and sidebar, and navigates to the selected page.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        st.logo(
            "Static\CASE LOGO.png",
        )
        cookies = self.controller.getAll()
        if st.session_state['loggedIn']==False:
            for key in cookies:
                if key.startswith("user_"):
                    st.session_state['user_id'] = cookies[key]
                    st.session_state['loggedIn']=True
                    st.toast(f"Welcome back, {get_name(st.session_state.user_id)}!",icon='🎉')
                    break
                

        if st.session_state['loggedIn']==False:
            self.login()
        else:
            st.sidebar.title(f"Hello {get_name(st.session_state.user_id)}")
            response=requests.post('http://41.33.183.2:4043/survey_exist',json={'user_id':str(st.session_state['user_id'])})
            print(response.json())
            if not response.json()['data']:
                    pg=st.navigation([self.pages[-1]])
                    pg.run()
            else:
                clicked=st.sidebar.button("Logout",on_click=self.logout)
                if not clicked:
                    placeholder=st.sidebar.empty()  
                    placeholder.selectbox("Market", ["USA","KSA"], key="market")
                    pg=st.navigation([self.pages[0],self.pages[3],self.pages[4],self.pages[5],self.pages[6]])
                    pg.run()

            
if __name__=='__main__':
    st.set_page_config(layout='wide')   
    controller = CookieController()
    full_app = MultiPageApp(controller=controller)
    # full_app.add_page("pages/About/about.py", title='Home')
    full_app.add_page('Displays/Login.py',title='Login')
    full_app.add_page('Displays/Signup.py',title='Signup')
    full_app.add_page("Displays/Datasets.py",title='My Projects') 
    full_app.run()



  