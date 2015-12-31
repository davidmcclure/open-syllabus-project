

import React, { Component } from 'react';
import Select from 'react-select';
import { connect } from 'react-redux';

import * as actions from '../actions/filters';
import { parseFilterValues } from '../utils';


@connect(
  state => ({
    filters: state.filters.filters
  }),
  actions,
)
export default class extends Component {


  /**
   * Render the corpus facets.
   */
  render() {
    return (
      <Select

        placeholder="All corpora"
        options={OSP.facets.corpus}
        value={this.props.filters.corpus}
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
    this.props.changeCorpusFilter(values);
  }


}
