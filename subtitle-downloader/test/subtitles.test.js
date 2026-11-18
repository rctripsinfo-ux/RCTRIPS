import { test } from 'node:test';
import assert from 'node:assert/strict';
import { convert, parseCues, wordCues } from '../lib/subtitles.js';
import { whisperToVtt } from '../lib/extractor.js';

const AUTO_VTT = `WEBVTT
Kind: captions
Language: en

00:00:00.160 --> 00:00:02.390 align:start position:0%
 
hello<00:00:00.560><c> everyone</c><00:00:00.880><c> and</c>

00:00:02.390 --> 00:00:02.400 align:start position:0%
hello everyone and


00:00:02.400 --> 00:00:04.950 align:start position:0%
hello everyone and
welcome<00:00:02.800><c> to</c><00:00:03.000><c> the</c><00:00:03.300><c> show</c>
`;

test('auto-generated rolling captions are deduplicated', () => {
  const srt = convert(AUTO_VTT, 'srt');
  assert.equal(srt, '1\n00:00:00,160 --> 00:00:02,390\nhello everyone and\n\n2\n00:00:02,400 --> 00:00:04,950\nwelcome to the show\n');
  assert.equal(convert(AUTO_VTT, 'txt'), 'hello everyone and\nwelcome to the show\n');
});

test('SRT input round-trips and entities/tags are cleaned', () => {
  const src = '1\r\n00:00:01,000 --> 00:00:02,500\r\n<i>Tom &amp; Jerry</i>\r\n\r\n2\r\n00:01:02,000 --> 00:01:03,000\r\nBye\r\n';
  assert.equal(convert(src, 'srt'), '1\n00:00:01,000 --> 00:00:02,500\nTom & Jerry\n\n2\n00:01:02,000 --> 00:01:03,000\nBye\n');
  assert.ok(convert(src, 'vtt').startsWith('WEBVTT\n\n00:00:01.000 --> 00:00:02.500\nTom & Jerry'));
});

test('short MM:SS.mmm timestamps parse', () => {
  const [c] = parseCues('WEBVTT\n\n01:02.500 --> 01:03.000\nHi');
  assert.deepEqual([c.start, c.end], [62500, 63000]);
});

test('empty input throws', () => {
  assert.throws(() => convert('WEBVTT\n', 'srt'), /No subtitle cues/);
});

test('word-level SRT uses inline word timestamps', () => {
  const { cues, exact } = wordCues(AUTO_VTT);
  assert.equal(exact, true);
  assert.deepEqual(cues.map((c) => c.lines[0]), ['hello', 'everyone', 'and', 'welcome', 'to', 'the', 'show']);
  assert.deepEqual(cues.slice(0, 3).map((c) => [c.start, c.end]), [[160, 560], [560, 880], [880, 2390]]);
  assert.deepEqual(cues.at(-1), { start: 3300, end: 4950, lines: ['show'] });
  assert.ok(convert(AUTO_VTT, 'words').startsWith('1\n00:00:00,160 --> 00:00:00,560\nhello\n'));
});

test('word-level SRT estimates timing when source has none', () => {
  const { cues, exact } = wordCues('WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nab cd');
  assert.equal(exact, false);
  assert.deepEqual(cues.map((c) => [c.start, c.end, c.lines[0]]), [[0, 500, 'ab'], [500, 1000, 'cd']]);
});

test('AI transcript is split into readable captions with exact word timings', () => {
  const w = (start, end, word) => ({ start, end, word });
  const vtt = whisperToVtt({ segments: [{ start: 0, end: 6, text: 'x', words: [
    w(0, 0.4, 'Hello'), w(0.4, 0.9, 'world.'), w(1.0, 1.3, 'This'), w(1.3, 1.6, 'is'), w(1.6, 2.0, 'a'),
    w(2.0, 2.5, 'test'), w(3.5, 4.0, 'after'), w(4.0, 4.5, 'pause'),
  ] }] });
  assert.equal(convert(vtt, 'srt'), '1\n00:00:00,000 --> 00:00:00,900\nHello world.\n\n2\n00:00:01,000 --> 00:00:02,500\nThis is a test\n\n3\n00:00:03,500 --> 00:00:04,500\nafter pause\n');
  const words = wordCues(vtt).cues;
  assert.equal(words.length, 8);
  assert.deepEqual([words[1].start, words[6].start, words[7].end], [400, 3500, 4500]);
});
