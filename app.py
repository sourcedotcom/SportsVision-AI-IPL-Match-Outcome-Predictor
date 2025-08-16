import streamlit as st
import pickle
import pandas as pd


teams = ['Sunrisers Hyderabad',
'Mumbai Indians',
'Royal Challengers Bangalore',
'Kolkata Knight Riders',
'Kings XI Punjab',
'Chennai Super Kings',
'Rajasthan Royals',
'Delhi Capitals',
'Gujrat Titans',
'Lucknow Supergiants']


cities = ['Hyderabad', 'Pune', 'Rajkot', 'Indore', 'Bangalore', 'Mumbai',
      'Kolkata', 'Delhi', 'Chandigarh', 'Kanpur', 'Jaipur', 'Chennai',
      'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion',
      'East London', 'Johannesburg', 'Kimberley', 'Bloemfontein',
      'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala', 'Kochi',
      'Visakhapatnam', 'Raipur', 'Ranchi', 'Abu Dhabi', 'Sharjah',
      'Mohali', 'Bengaluru']


pipe = pickle.load(open('pipe.pkl','rb'))
st.title('IPL The Victory Vision')


col1, col2 = st.columns(2)


with col1:
   batting_team = st.selectbox('Select the batting team',sorted(teams))
with col2:
   available_bowling_teams = [team for team in sorted(teams) if team != batting_team]
   bowling_team = st.selectbox('Select the bowling team', available_bowling_teams)

selected_city = st.selectbox('Select host city',sorted(cities))

target = st.number_input('Target', min_value=1, step=1)

col3,col4,col5,col6 = st.columns(4)


with col3:
   score = st.number_input('Score', min_value=0, step=1)
with col4:
   wickets = st.number_input('Wickets out', min_value=0, max_value=10, format="%d")
with col5:
   overs = st.number_input('Overs completed', min_value=0, max_value=19,step=1, format="%d")
with col6:
   balls = st.number_input('Balls completed', min_value=0, max_value=6,step=1, format="%d")


# Create a checkbox
agree_checkbox = st.checkbox("All the input feilds are correctly filled")

# Create a button and disable it until checkbox is checked
if agree_checkbox:
   button_disabled = False 
else:
   button_disabled = True 

  
if st.button('Predict Probability', disabled=button_disabled):
   if ((score >= target+6) or (score >= target and wickets == 10)):
      st.header("Invalid Combinations")
         
   elif ((score < target) and (wickets > 10 or ((overs*6 + balls) > 120))):
      st.header("Invalid Combinations")
         
   elif score >= target:
      st.header(batting_team + " won the match")
      st.header(bowling_team + " lost the match")

   elif ((((overs*6 + balls)== 120) and (score==target-1)) or ((score==target-1) and (wickets==10))):
      st.header("Match Tied")
      
   elif (((overs*6 + balls)== 120 and score < target-1) or ((score<target-1) and (wickets==10))):
      st.header(batting_team + " lost the match")
      st.header(bowling_team + " won the match")
         
   else :
      runs_left = target - score
      balls_left = 120 - overs * 6 - balls
      wickets = 10 - wickets
      if overs != 0:
         crr = (score*6)/(120 - balls_left)
      else:
         crr = 0  
      if balls_left > 0:
         rrr = (runs_left*6)/balls_left
      else :
         rrr = 0

            
      input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets_left':[wickets],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})

      
      result = pipe.predict_proba(input_df)
      loss = result[0][0]
      win = result[0][1]
      st.header(batting_team + "- " + str(round(win*100)) + "%")
      st.header(bowling_team + "- " + str(round(loss*100)) + "%")
      