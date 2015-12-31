

import React, { Component } from 'react';
import Select from 'react-select';


export default class extends Component {


  /**
   * Render the corpus facets.
   */
  render() {
    return (
      <Select
        placeholder="All corpora"
        options={OSP.facets.corpus}
        onChange={this.onChange.bind(this)}
      />
    );
  }


  /**
   * When the selection is changed.
   *
   * @param {Object} option
   */
  onChange(option) {
    console.log(option);
  }


}
