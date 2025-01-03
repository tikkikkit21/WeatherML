# WeatherML
## Background
The idea for this project started when I was a first-year college student at
Virginia Tech (VT). As someone living on-campus, I had to walk across the
Drillfield to get to my classes. As a result, I got in the habit of checking the
weather every time when I had to go somewhere (I even ended up adding a
temperature widget to my lock screen since I checked the weather so many times).
The problem was that predicting my choice of clothing wasn't straightforward.
There would be days when I could go out with just a T-shirt when it was only
65°F. On others, I would need a coat even though it was 73°F.

Obviously, temperature is not the only factor in comfort. Wind, humidity, and
whether the sun is shining can all affect how warm or cold I feel. However, it's
very hard for me to make a prediction while juggling all the different factors.
As a result, I thought about potentially coding some sort of AI that could read
the weather and give me a prediction on what I should wear outside. Thus, the
idea for *WeatherML* was born.

## Data Collection
At the start, I didn't have any experience or knowledge to code a ML model.
However, I knew I would need a lot of data, so I started collecting data right
away. I included as many factors that I thought might be relevant, and tried to
collect several times a day (morning, noon, evening). My source of data was just
the Weather app on my iPhone. Although I've heard that it's not the most
accurate source for weather information, it was the most convenient for me.
Besides, I used the Weather app anyways to check the weather so I trusted that
the ML model would be able to handle the inaccuracies. I recorded my data in
[this Google sheet](https://docs.google.com/spreadsheets/d/1wjoOM3OyRlOUdET7_jU2uoCyOraQOWY8XGOw8LVWK3A)
and then downloaded it as a CSV file when I was ready to begin working.

## Learning Journey
I started my AI learning journey with an introductory course at VT: *CS4804:
Intro to Artificial Intelligence*. However, this course was more focused on
concepts and theory rather than practical applications. As a result, I turned to
LinkedIn Learning courses (check out my [LinkedInLearning](https://github.com/tikkikkit21/LinkedInLearning)
repository for notes and exercise files from courses I've taken. Most of the ML
courses are under the *Python* folder). As I took more classes at VT and
LinkedIn Learning, my skills improved. Each class I took would introduce me to
something new that I wanted to integrate in this project. This repository is
actually the second iteration of this project. I had learned so much since the
beginning of this project's development that I decided to completely overhaul my
entire codebase.

## Technical Implementation
I use `pandas` and `numpy` for data processing and `scikit-learn` for ML models.
This project mainly consists of 2 phases.

The first phase is my research. I analyze the data I've collected and experiment
with different analysis and visualization techniques. Next, I try out different
ML models and play around with their respective hyperparameters. In the end, I
decide which model is the best for my project. I presented all my work in a single Jupyter Notebook.

The second phase is the runner program. This program uses native Python to set
up my final ML model so I can make predictions on real world examples. For now,
it's just a program that's run on the command line. However, I hope to set up
some sort of user interface in the future, making it easier to directly interact
with the model.
