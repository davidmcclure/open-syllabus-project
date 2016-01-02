

import _ from 'lodash';
import React, { Component, PropTypes } from 'react';
import Select from 'react-select';
import pluralize from 'pluralize';

import { parseFilterValues } from '../utils';


export default class extends Component {


  static propTypes = {
    name: PropTypes.string.isRequired,
    options: PropTypes.array.isRequired,
    value: PropTypes.any,
    publish: PropTypes.func.isRequired,
  }


  /**
   * Render the select widget.
   */
  render() {

    pluralize.addIrregularRule('corpus', 'corpora');

    let plural = pluralize(this.props.name, 2);

    return (
      <div className="filter-control">

        <h5>Filter by {this.props.name}</h5>

        <Select

          options={this.props.options}
          value={this.props.value}
          placeholder={`All ${plural}`}
          multi={true}

          onChange={this.onChange.bind(this)}

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
    let values = _.pluck(options, 'value')
    this.props.publish(values);
  }


}
