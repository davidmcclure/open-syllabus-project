

import React, { Component } from 'react';


export default class extends Component {


  /**
   * Render the header.
   */
  render() {
    return (
      <div id="header">

        <h1>
          <a href="/">Open Syllabus Explorer</a>
          <code>beta</code>
        </h1>

        <p>The top ~10,000 texts. Texts assigned on the same syllabi are
        clustered together.</p>

      </div>
    );
  }


}
