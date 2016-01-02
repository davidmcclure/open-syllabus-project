

import React, { Component } from 'react';


export default class extends Component {


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
          onKeyPress={this.onKeyPress.bind(this)}
        />

      </div>
    );
  }


  /**
   * Search when "Enter" is pressed.
   *
   * @param {Object} e
   */
  onKeyPress(e) {
    if (e.key == 'Enter') {
      console.log('search');
    }
  }


}
