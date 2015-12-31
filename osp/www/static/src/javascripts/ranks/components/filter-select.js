

import React, { Component } from 'react';
import Select from 'react-select';

import { parseFilterValues } from '../utils';


export default class extends Component {


  /**
   * Render the select widget.
   */
  render() {
    return (
      <Select

        options={this.props.options}
        value={this.props.value}
        placeholder={this.props.placeholder}
        multi={true}

        onChange={this.onChange.bind(this)}

      />
    );
  }


  /**
   * When the selection is changed.
   *
   * @param {Array} options
   */
  onChange(options) {
    let values = parseFilterValues(options);
    this.props.publish(values);
  }


}
