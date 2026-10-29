from src.tp3.utils.config import output_logger


def test_output_logger_ecrit_sur_stdout_sans_prefixe(capsys):
    # Given / When
    output_logger.info("[+] FLAG1: ESGI{test}")

    # Then
    captured = capsys.readouterr()
    assert captured.out == "[+] FLAG1: ESGI{test}\n"
