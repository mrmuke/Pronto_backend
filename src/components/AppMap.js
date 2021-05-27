import React from 'react'

import { compose, withProps, lifecycle } from "recompose";
import {
  withScriptjs,
  withGoogleMap,
  GoogleMap,
  DirectionsRenderer
} from "react-google-maps";
//sometimes walking sometimes driving
const AppMap = compose(
  withProps(props=>({
    googleMapURL: "https://maps.googleapis.com/maps/api/js?key=AIzaSyAPOOnlu8YXdWsyM3uUkz3tU7AeDWgoQqA&v=3.exp&libraries=geometry,drawing,places",
    loadingElement: <div style={{ height: `100%` }} />,
    containerElement: <div style={{ height: props.height+"px"/* ""+(104+props.places.length*71)+"px" */,border:'2px solid #ccc' ,width:'100%'}} />,
    mapElement: <div style={{ height: `100%` }} />,
  })),
  withScriptjs,
  withGoogleMap,
  lifecycle({
    componentDidMount() {
      const DirectionsService = new window.google.maps.DirectionsService();

      const origin = this.props.places[0];
      const destination = this.props.places[this.props.places.length-1];
      const waypoints = [] 
      //add hotel
      for( var i = 1;i<this.props.places.length-1;i++){
        var place= this.props.places[i]
        waypoints.push({
          location:new window.google.maps.LatLng(place.lat,place.lng)
        })
      }

      DirectionsService.route({
        origin: new window.google.maps.LatLng(origin.lat, origin.lng),
        destination: new window.google.maps.LatLng(destination.lat, destination.lng),
        waypoints:waypoints,
        travelMode: window.google.maps.TravelMode.DRIVING,
        
      }, (result, status) => {
        console.log(result)
        if (status === window.google.maps.DirectionsStatus.OK) {
          this.setState({
            directions: result,
          });
        } else {
          console.error(result)
          console.error(`error fetching directions ${result}`);
        }
      });
    }
  })
)(props =>
  <GoogleMap
    defaultZoom={7}
    defaultCenter={new window.google.maps.LatLng(41.8507300, -87.6512600)}
  >
    {props.directions && <DirectionsRenderer directions={props.directions} />}
  </GoogleMap>
);
export default AppMap