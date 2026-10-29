from src.tp3 import main as main_module


def test_main_affiche_les_deux_drapeaux(monkeypatch, capsys):
    # Given
    monkeypatch.setattr("sys.argv", ["tp3", "--target", "http://cible"])
    monkeypatch.setattr(main_module, "breach_web", lambda target: ("1.2.3.4", 9090, "deadbeef", "ESGI{web_test}"))
    monkeypatch.setattr(main_module, "breach_network", lambda host, port, key: "ESGI{chain_test}")

    # When
    main_module.main()

    # Then
    captured = capsys.readouterr()
    assert "ESGI{web_test}" in captured.out
    assert "ESGI{chain_test}" in captured.out
