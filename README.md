# Flood Fill
## Inspiration
Flooding is Canada's most common and most expensive natural disaster. At the same time, Canadian real estate prices are always increasing. Canadians need a way to predict whether a property will be underwater in the next 30 years before purchasing it.
## What it does
Flood Fill is a web app that allows users to input an address using an integrated Google Map and generate a report of its current flood risk and projected flood risks by 2100.
## How we built it
In the backend, we created a Neural Net using Python and TensorFlow and trained it using precipitation and flooding data. We developed the frontend using React and Tailwind, which features an interactive Google Map and an autocompleting search bar.
## Challenges we ran into
We had a lot of trouble finding a suitable dataset for flooding, as flooded areas were never exact. We ended up having to do lots of computation ourselves to determine the area of floods.
## Accomplishments that we're proud of
Managing to wrangle over 100 million data points to work with our model to predict as best we can!
## What we learned
Data is one of the hardest parts of a project like this (slogging through api docs, formatting data...)
## What's next for Flood Fill
Things to improve for Flood Fill :
<ul>
<li> Develop Flood Fill into a web extension! </li>
<li> Improve the tuning of the model (and add more features) </li>
</ul>

## Data Sources
- [Historical Flood Events | Natural Resources Canada](https://open.canada.ca/data/en/dataset/fe83a604-aa5a-4e46-903c-685f8b0cc33c/resource/73306f3d-8367-463e-899a-7a3854e6b2ab)
- [CanDCS-U6 Precipitation History & Predictions | Environment and Climate Change Canada](https://open.canada.ca/data/en/dataset/f73d6939-912a-4add-a291-c233fc5d1946)
