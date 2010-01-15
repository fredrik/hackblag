require 'rubygems'
require 'wukong'

module JeanSizes
  class Mapper < Wukong::Streamer::LineStreamer
    def process(line)
      fields = line.strip.split("\t")
      country = fields[3]
      sizes   = fields[11..23]
      yield [country, sizes] if sizes.length == 13
    end
  end
  class Reducer < Wukong::Streamer::ListReducer
    def finalize
      sums = values.pop[1..-1].map(&:to_i)
      for v in values 
        sizes = v[1..-1].map(&:to_i)
        sums = sums.zip(sizes).map {|x| x.sum}
      end
      yield [key, sums]
    end
  end
end

Wukong::Script.new(JeanSizes::Mapper, JeanSizes::Reducer).run
