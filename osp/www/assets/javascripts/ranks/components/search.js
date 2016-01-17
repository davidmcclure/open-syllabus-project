

import _ from 'lodash';
import React, { Component } from 'react';
import classNames from 'classnames';
import { connect } from 'react-redux';

import * as actions from '../actions/filters';


@connect(
  state => state.filters,
  actions,
)
export default class extends Component {


  /**
   * Set initial state.
   *
   * @param {Object} props
   */
  constructor(props) {

    super(props);

    this.state = {
      query: ''
    };

  }


  /**
   * When the query is changed from without, update the input.
   *
   * @param {Object} newProps
   */
  componentWillReceiveProps(newProps) {

    this.setState({
      query: newProps.query
    });

  }


  /**
   * Render the search box.
   */
  render() {

    let btnCx = classNames('btn', 'btn-default', 'btn-lg');

    return (
      <div id="search" className="input-group">

        <input

          className="form-control input-lg"
          placeholder="Filter by title, author, journal, etc."
          onKeyPress={this.onKeyPress.bind(this)}

          valueLink={{
            value: this.state.query,
            requestChange: this.onChange.bind(this),
          }}

        />

        <span className="input-group-btn">

          <button
            className={btnCx}
            onClick={this.clear.bind(this)}>
            <i className="fa fa-times"></i>
          </button>

          <button
            className={btnCx}
            onClick={this.search.bind(this)}>
            {'Search'}
          </button>

        </span>

      </div>
    );

  }


  /**
   * Clean the new value, update state.
   *
   * @param {String} query
   */
  onChange(query) {
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
    this.props.changeFilters({
      query: this.state.query
    });
  }


  /**
   * Clear the query.
   */
  clear() {
    this.setState({ query: '' }, () => {
      this.search();
    });
  }


}
