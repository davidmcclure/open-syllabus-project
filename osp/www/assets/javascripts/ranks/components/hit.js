

import _ from 'lodash';
import chroma from 'chroma-js';

import config from './hit.yml';


export default class {


  /**
   * Set the raw hit.
   *
   * @param {Object} hit
   */
  constructor(hit) {
    this.hit = hit;
  }


  /**
   * Get a document field.
   *
   * @param {String} key
   * @return {String}
   */
  field(key, delimiter=', ') {

    // Try to find a highlight.
    let value = (
      _.get(this.hit, `highlight.${key}`) ||
      _.get(this.hit, `_source.${key}`)
    );

    // Join arrays into a string.
    return _.isArray(value) ? value.join(delimiter) : value;

  }


  /**
   * Build the text profile path.
   *
   * @return {String}
   */
  get path() {

    let c = this.hit._source.corpus;
    let i = this.hit._source.identifier;

    return `text/${c}/${i}`;

  }


  /**
   * Get the citation count.
   *
   * @return {Number}
   */
  get count() {
    return this.hit.sort[0].toLocaleString();
  }


  /**
   * Get the overall rank.
   *
   * @return {Number}
   */
  get rank() {
    return this.field('rank').toLocaleString();
  }


  /**
   * Get the teaching score.
   *
   * @return {Number}
   */
  get score() {
    return (this.field('score')*100).toFixed(1);
  }


  /**
   * Get a green -> red scoring color.
   *
   * @return {String}
   */
  get color() {

    let scale = chroma.scale([
      config.colors.low,
      config.colors.high,
    ]).mode('lab');

    return scale(this.field('score')).hex()

  }


}
