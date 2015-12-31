

import React, { Component } from 'react';
import Select from 'react-select';


export default class extends Component {


  /**
   * Render the institution facets.
   */
  render() {
    return (
      <Select
        placeholder="All institutions"
        options={OSP.facets.institution}
      />
    );
  }


}
