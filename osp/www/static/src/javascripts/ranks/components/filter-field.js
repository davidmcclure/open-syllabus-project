

import React, { Component } from 'react';
import Select from 'react-select';
import { connect } from 'react-redux';

import * as actions from '../actions/filters';
import { parseFilterValues } from '../utils';


@connect(
  state => ({
    filters: state.filters
  }),
  actions,
)
export default class extends Component {


  /**
   * Render the field facets.
   */
  render() {
    return (
      <Select

        placeholder="All fields"
        options={OSP.facets.field}
        value={this.props.filters.field_id}
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
    this.props.changeFieldFilter(values);
  }


}
