#include "font.h"

#include "esphome/core/hal.h"
#include "esphome/core/log.h"
#include "esphome/core/color.h"
#include "esphome/components/display/display_buffer.h"

namespace esphome {
namespace font {

static const char *const TAG = "font";

const uint8_t *Glyph::get_char() const { return this->glyph_data_->a_char; }
// Compare the char at the string position with this char.
// Return true if this char is less than or equal the other.
bool Glyph::compare_to(const uint8_t *str) const {
  // 1 -> this->char_
  // 2 -> str
  for (uint32_t i = 0;; i++) {
    if (this->glyph_data_->a_char[i] == '\0')
      return true;
    if (str[i] == '\0')
      return false;
    if (this->glyph_data_->a_char[i] > str[i])
      return false;
    if (this->glyph_data_->a_char[i] < str[i])
      return true;
  }
  // this should not happen
  return false;
}
int Glyph::match_length(const uint8_t *str) const {
  for (uint32_t i = 0;; i++) {
    if (this->glyph_data_->a_char[i] == '\0')
      return i;
    if (str[i] != this->glyph_data_->a_char[i])
      return 0;
  }
  // this should not happen
  return 0;
}
void Glyph::scan_area(int *x1, int *y1, int *width, int *height) const {
  *x1 = this->glyph_data_->offset_x;
  *y1 = this->glyph_data_->offset_y;
  *width = this->glyph_data_->width;
  *height = this->glyph_data_->height;
}

Font::Font(const GlyphData *data, int data_nr, int baseline, int height, uint8_t bpp)
    : baseline_(baseline), height_(height), bpp_(bpp) {
  glyphs_.reserve(data_nr);
  for (int i = 0; i < data_nr; ++i)
    glyphs_.emplace_back(&data[i]);
}
int Font::match_next_glyph(const uint8_t *str, int *match_length) {
  int lo = 0;
  int hi = this->glyphs_.size() - 1;
  while (lo != hi) {
    int mid = (lo + hi + 1) / 2;
    if (this->glyphs_[mid].compare_to(str)) {
      lo = mid;
    } else {
      hi = mid - 1;
    }
  }
  *match_length = this->glyphs_[lo].match_length(str);
  if (*match_length <= 0)
    return -1;
  return lo;
}
void Font::measure(const char *str, int *width, int *x_offset, int *baseline, int *height) {
  *baseline = this->baseline_;
  *height = this->height_;
  int i = 0;
  int min_x = 0;
  bool has_char = false;
  int x = 0;
  while (str[i] != '\0') {
    int match_length;
    int glyph_n = this->match_next_glyph((const uint8_t *) str + i, &match_length);
    if (glyph_n < 0) {
      // Unknown char, skip
      if (!this->get_glyphs().empty())
        x += this->get_glyphs()[0].glyph_data_->width;
      i++;
      continue;
    }

    const Glyph &glyph = this->glyphs_[glyph_n];
    if (!has_char) {
      min_x = glyph.glyph_data_->offset_x;
    } else {
      min_x = std::min(min_x, x + glyph.glyph_data_->offset_x);
    }
    x += glyph.glyph_data_->width + glyph.glyph_data_->offset_x;

    i += match_length;
    has_char = true;
  }
  *x_offset = min_x;
  *width = x - min_x;
}
void Font::print(int x_start, int y_start, display::Display *display, Color color, const char *text, Color background) {
  int i = 0;
  int x_at = x_start;
  int scan_x1, scan_y1, scan_width, scan_height;
  while (text[i] != '\0') {
    int match_length;
    int glyph_n = this->match_next_glyph((const uint8_t *) text + i, &match_length);
    if (glyph_n < 0) {
      // Unknown char, skip
      ESP_LOGW(TAG, "Encountered character without representation in font: '%c'", text[i]);
      if (!this->get_glyphs().empty()) {
        uint8_t glyph_width = this->get_glyphs()[0].glyph_data_->width;
        display->filled_rectangle(x_at, y_start, glyph_width, this->height_, color);
        x_at += glyph_width;
      }

      i++;
      continue;
    }

    const Glyph &glyph = this->get_glyphs()[glyph_n];
    glyph.scan_area(&scan_x1, &scan_y1, &scan_width, &scan_height);

    const uint8_t *data = glyph.glyph_data_->data;
    const int max_x = x_at + scan_x1 + scan_width;
    const int max_y = y_start + scan_y1 + scan_height;

    uint8_t bitmask = 0;
    uint8_t pixel_data = 0;
    float bpp_max = (1 << this->bpp_) - 1;
    for (int glyph_y = y_start + scan_y1; glyph_y != max_y; glyph_y++) {
      for (int glyph_x = x_at + scan_x1; glyph_x != max_x; glyph_x++) {
        uint8_t pixel = 0;
        for (int bit_num = 0; bit_num != this->bpp_; bit_num++) {
          if (bitmask == 0) {
            pixel_data = progmem_read_byte(data++);
            bitmask = 0x80;
          }
          pixel <<= 1;
          if ((pixel_data & bitmask) != 0)
            pixel |= 1;
          bitmask >>= 1;
        }
        if (pixel == bpp_max) {
          display->draw_pixel_at(glyph_x, glyph_y, color);
        } else if (pixel != 0) {
          float on = (float) pixel / bpp_max;
          float off = 1.0 - on;
          Color blended;
          blended.r = color.r * on + background.r * off;
          blended.g = color.r * on + background.g * off;
          blended.b = color.r * on + background.b * off;
          display->draw_pixel_at(glyph_x, glyph_y, blended);
        }
      }
    }
    x_at += glyph.glyph_data_->width + glyph.glyph_data_->offset_x;

    i += match_length;
  }
}

}  // namespace font
}  // namespace esphome
