

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
      <div className="filter-control">

        <h5>Search texts</h5>

        <input

          className="form-control"
          placeholder="Title, author, publisher, etc."

          value={this.state.query}
          onChange={this.onChange.bind(this)}
          onKeyPress={this.onKeyPress.bind(this)}

        />

      </div>
    );
  }


  /**
   * Input -> state.
   *
   * @param {Object} e
   */
  onChange(e) {
    let query = e.target.value.trim() || null;
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
