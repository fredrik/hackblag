require 'rubygems'
require 'wukong'

module Normalize
  class Mapper < Wukong::Streamer::LineStreamer
    def process(line)
      fields = line.strip.split("\t")
      country = fields.reverse!.pop
      data = fields.map(&:to_i)
      sum = data.sum.to_f
      normalized = data.map {|x| 100 * x/sum }
      s = normalized.join(",")
      yield [country, s]
    end
  end
end

Wukong::Script.new(Normalize::Mapper, nil).run
