

import _ from 'lodash';
import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import Select from 'react-select';
import pluralize from 'pluralize';

import * as actions from '../actions/filters';
import FilterOption from './filter-option';


@connect(null, actions)
export default class extends Component {


  static propTypes = {
    filter: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    options: PropTypes.array.isRequired,
    value: PropTypes.array.isRequired,
  };


  /**
   * Render the select widget.
   */
  render() {

    pluralize.addIrregularRule('corpus', 'corpora');

    let plural = pluralize(this.props.name, 2);

    return (
      <div className="filter-control">

        <h4>Filter by {this.props.name}</h4>

        <Select

          options={this.props.options}
          value={this.props.value}
          placeholder={`All ${plural}`}
          multi={true}

          onChange={this.onChange.bind(this)}

          optionRenderer={function(o) {
            return <FilterOption option={o} />;
          }}

        />

      </div>
    );

  }


  /**
   * When the selection is changed.
   *
   * @param {Array} options
   */
  onChange(options) {

    let values = _.map(options, 'value');

    this.props.changeFilters({
      [this.props.filter]: values
    });

  }


}
