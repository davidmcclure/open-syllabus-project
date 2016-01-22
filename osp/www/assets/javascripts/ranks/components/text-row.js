

import React, { Component, PropTypes } from 'react';

import Hit from './hit';
import Field from './field';


export default class extends Component {


  static propTypes = {
    hit: PropTypes.object.isRequired,
    rank: PropTypes.number.isRequired,
  };


  /**
   * Render a text row.
   */
  render() {

    this.hit = new Hit(this.props.hit);

    let scoreStyle = {
      color: this.hit.color
    }

    return (
      <tr className="text-row">

        <td className="rank">
          {this.props.rank}
        </td>

        <td className="count">
          {this.hit.count}
        </td>

        <td className="score" style={scoreStyle}>
          {this.hit.score}
        </td>

        <td className="text">

          <a href={this.hit.path}>
            <div className="title" dangerouslySetInnerHTML={{
              __html: this.hit.field('title')
            }}></div>
          </a>

          <Field
            label="author"
            value={this.hit.field('authors')}
          />

          <Field
            label="journal"
            value={this.hit.field('journal')}
          />

        </td>

      </tr>
    );

  }


}
