

import React, { Component, PropTypes } from 'react';


export default class extends Component {


  static contextTypes = {
    map: PropTypes.object.isRequired,
  };


  /**
   * Mount the field boxes.
   */
  componentDidMount() {
    console.log('fields');
  }


  render() {
    return null;
  }


}
