from src.tp2.main import main


def test_main(tmp_path, monkeypatch):
    samples = tmp_path / "samples"
    samples.mkdir()
    (samples / "a.bin").write_bytes(b"http://c2.example.test/x")
    regles = tmp_path / "rules"
    regles.mkdir()
    out = tmp_path / "out"
    monkeypatch.setattr(
        "sys.argv",
        ["tp2", "--samples", str(samples), "--rules", str(regles), "--out", str(out)],
    )

    main()

    assert len(list(out.glob("*.json"))) == 2