

import React, { Component } from 'react';

import Leader from './leader';
import Image from './image';


export default class extends Component {


  /**
   * Render the application.
   */
  render() {
    return (
      <div className="wrapper">

        <div id="header">
          <Leader />
        </div>

        <Image />

      </div>
    );
  }


}
