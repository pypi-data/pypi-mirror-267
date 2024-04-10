extern crate nafcodec;

use std::io::Cursor;

use nafcodec::Decoder;
use nafcodec::EncoderBuilder;
use nafcodec::Flag;
use nafcodec::Record;
use nafcodec::SequenceType::Dna;

fn test_records() -> Vec<Record> {
    vec![
        Record {
            id: Some(String::from("r1")),
            comment: Some(String::from("record 1")),
            sequence: Some(String::from("NGCTCTTAAACCTGCTA")),
            quality: Some(String::from("#8CCCGGGGGGGGGGGG")),
            length: Some(17),
        },
        Record {
            id: Some(String::from("r2")),
            comment: Some(String::from("record 2")),
            sequence: Some(String::from("NTAATAAGCAATGACGGCAGC")),
            quality: Some(String::from("#8AACCFF<FFGGFGE@@@@@")),
            length: Some(21),
        },
    ]
}

#[test]
pub fn encode_id() {
    let mut encoder = EncoderBuilder::from_flags(Dna, Flag::Id)
        .with_memory()
        .unwrap();

    let records = test_records();
    encoder.push(&records[0]).unwrap();
    encoder.push(&records[1]).unwrap();

    let mut buffer = Vec::new();
    encoder.write(&mut buffer).unwrap();

    let mut decoder = Decoder::new(Cursor::new(buffer)).unwrap();
    assert!(decoder.header().flags().test(Flag::Id));
    assert!(!decoder.header().flags().test(Flag::Comment));
    assert!(!decoder.header().flags().test(Flag::Sequence));
    assert!(!decoder.header().flags().test(Flag::Quality));

    let r1 = decoder.next().unwrap().unwrap();
    assert_eq!(r1.id, Some(String::from("r1")));
    assert!(r1.comment.is_none());
    assert!(r1.sequence.is_none());
    assert!(r1.quality.is_none());
    assert!(r1.length.is_none());

    let r2 = decoder.next().unwrap().unwrap();
    assert_eq!(r2.id, Some(String::from("r2")));
    assert!(r2.comment.is_none());
    assert!(r2.sequence.is_none());
    assert!(r2.quality.is_none());
    assert!(r2.length.is_none());
}

#[test]
pub fn encode_id_sequence() {
    let mut encoder = EncoderBuilder::from_flags(Dna, Flag::Id | Flag::Sequence)
        .with_memory()
        .unwrap();

    let records = test_records();
    encoder.push(&records[0]).unwrap();
    encoder.push(&records[1]).unwrap();

    let mut buffer = Vec::new();
    encoder.write(&mut buffer).unwrap();

    let mut decoder = Decoder::new(Cursor::new(buffer)).unwrap();
    assert!(decoder.header().flags().test(Flag::Id));
    assert!(!decoder.header().flags().test(Flag::Comment));
    assert!(decoder.header().flags().test(Flag::Sequence));
    assert!(!decoder.header().flags().test(Flag::Quality));

    let r1 = decoder.next().unwrap().unwrap();

    assert_eq!(r1.id, Some(String::from("r1")));
    assert!(r1.comment.is_none());
    assert_eq!(r1.sequence, Some(String::from("NGCTCTTAAACCTGCTA")));
    assert!(r1.quality.is_none());
    assert!(r1.length.is_some());

    let r2 = decoder.next().unwrap().unwrap();
    assert_eq!(r2.id, Some(String::from("r2")));
    assert!(r2.comment.is_none());
    assert_eq!(r2.sequence, Some(String::from("NTAATAAGCAATGACGGCAGC")));
    assert!(r2.quality.is_none());
    assert!(r2.length.is_some());
}

#[test]
pub fn encode_quality() {
    let mut encoder = EncoderBuilder::new(Dna)
        .quality(true)
        .sequence(false)
        .id(false)
        .with_memory()
        .unwrap();

    let records = test_records();
    encoder.push(&records[0]).unwrap();
    encoder.push(&records[1]).unwrap();

    let mut buffer = Vec::new();
    encoder.write(&mut buffer).unwrap();

    let mut decoder = Decoder::new(Cursor::new(buffer)).unwrap();
    println!("{:?}", decoder.header());
    assert!(!decoder.header().flags().test(Flag::Id));
    assert!(!decoder.header().flags().test(Flag::Comment));
    assert!(!decoder.header().flags().test(Flag::Sequence));
    assert!(decoder.header().flags().test(Flag::Quality));

    let r1 = decoder.next().unwrap().unwrap();
    assert!(r1.id.is_none());
    assert!(r1.comment.is_none());
    assert!(r1.sequence.is_none());
    assert_eq!(r1.quality, Some(String::from("#8CCCGGGGGGGGGGGG")));
    assert!(r1.length.is_some());

    let r2 = decoder.next().unwrap().unwrap();
    assert!(r2.id.is_none());
    assert!(r2.comment.is_none());
    assert!(r2.sequence.is_none());
    assert_eq!(r2.quality, Some(String::from("#8AACCFF<FFGGFGE@@@@@")));
    assert!(r2.length.is_some());
}
