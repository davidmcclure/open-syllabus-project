

import React, { Component } from 'react';
import Select from 'react-select';


export default class extends Component {


  /**
   * Render the state facets.
   */
  render() {
    return (
      <Select
        placeholder="All states"
        options={OSP.facets.state}
      />
    );
  }


}
