

import _ from 'lodash';


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
   * Get the citation count.
   *
   * @return {Number}
   */
  count() {
    return this.hit.sort[0];
  }


  /**
   * Get a document field. (Highlighted, if present.)
   *
   * @param {String} key
   * @return {String}
   */
  field(key) {
    return (
      _.get(this.hit, `highlight.${key}`) ||
      _.get(this.hit, `_source.${key}`)
    );
  }


}
