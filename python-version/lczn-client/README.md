# Lczn Client
This part is a simple web application used to render the estimate location, real location and round trip delay.
## About React
You can see an introduction about react [here](https://reactjs.org/docs/react-component.html)

In this application, we utilized react component to construct web page.

**The Component Lifecycle:**

These methods are called when an instance of a component is being created and inserted into the DOM:
```
constructor()
componentWillMount()
render()
componentDidMount()
```
where 

constructor() used to initial private class variable, 

componentWillMount() used to update them, 

and render() return a html segment.



## Structure
Firstly, I'd like to break The UI Into a component hierarchy.A component should ideally only do one thing. If it ends up growing, it should be decomposed into smaller subcomponents.

So in our application, main component is App.js, it include three children: Subscribe.js, Location.js, Floor.js.

 **App.js:**   Control the three children component and record private variables  such as channel number, a list of received message, estimate location and real location in latest message

**Subscribe :** Render a select dropdown using [react-select](https://github.com/JedWatson/react-select) and submit button. Select the channel you want to listen after click "Submit" button

**Floor :** Render estimate location  and real location in grid using [react-highchart](https://github.com/kirjs/react-highcharts)

**Location :** Display round trip delay,  real location and  estimate location in a list

![structure](../images/lczn-client.png)
## Sample Output

![sample output](../images/browser_sample.png)