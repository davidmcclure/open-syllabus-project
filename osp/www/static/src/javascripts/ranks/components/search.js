

import _ from 'lodash';
import React, { Component } from 'react';
import { connect } from 'react-redux';

import * as actions from '../actions/filters';


@connect(null, actions)
export default class extends Component {


  /**
   * Set initial state.
   *
   * @param {Object} props
   */
  constructor(props) {

    super(props);

    this.state = {
      query: null
    };

  }


  /**
   * Render the search box.
   */
  render() {
    return (
      <div id="search">

        <input

          className="form-control input-lg"
          placeholder="Filter by title, author, journal, etc."

          valueLink={{
            value: this.state.query,
            requestChange: this.onChange.bind(this),
          }}

          onKeyPress={this.onKeyPress.bind(this)}

        />

      </div>
    );
  }


  /**
   * Clean the new value, update state.
   *
   * @param {String} newVal
   */
  onChange(newVal) {
    let query = newVal.trim() || null;
    this.setState({ query });
  }


  /**
   * Search when "Enter" is pressed.
   *
   * @param {Object} e
   */
  onKeyPress(e) {
    if (e.key == 'Enter') {
      this.search();
    }
  }


  /**
   * Apply the current query.
   */
  search() {
    this.props.changeSearchQuery(this.state.query);
  }


}
