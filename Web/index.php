<!DOCTYPE html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link rel="stylesheet" type="text/css" href="css/util.css">
        <link rel="stylesheet" type="text/css" href="css/main.css">
        <link href="css/btn.css" rel="stylesheet" type="text/css" />
    </head>
    <body>
        <br><br><br>
        <CENTER>


        <div class="limiter">
            <div class="wrap-table100">
                <div class="table">
                    <div class="row header">

        <?php
            $conn = mysqli_connect('localhost', 'root', '11223344', 'PillBox');
            if ( !$conn ) die('DB Error');

            $sql1 = "SELECT * FROM patient_pillbox"; 
            $rs1 = mysqli_query($conn, $sql1);

            echo '<div class="cell">약통 이름</div>' .
                '<div class="cell">환자 번호</div>' .
                '<div class="cell">환자 이름</div>' .
                '<div class="cell">생년월일</div></div>';

                while($info1 = mysqli_fetch_array($rs1))
                {
                    $sql2 = "SELECT * FROM pillbox_no where B_ID ='" . $info1['B_ID'] . "'"; 
                    $rs2 = mysqli_query($conn, $sql2);

                    while($info2 = mysqli_fetch_array($rs2))
                    {
                        $sql3 = "SELECT * FROM patient_info where P_ID =" . $info1['P_ID'] . ""; 
                        $rs3 = mysqli_query($conn, $sql3);
                        
                        while($info3 = mysqli_fetch_array($rs3))
                        {
                            #각 열을 하나하나 불러와서 표 만들기
                            echo '<div class="row"><div class="cell" data-title="약통 이름">' . $info2['B_NAME'] . '</div>' .
                                '<div class="cell" data-title="환자 이름">' . $info3['P_ID'] . '</div>' .
                                '<div class="cell" data-title="환자 이름">' . $info3['P_NAME'] . '</div>' .
                                '<div class="cell" data-title="생년월일">' . $info3['P_BIRTHDATE'] . '</div></div>';
                        }      
                    }
                }
                echo '</div></div></div><br><br>';

            mysqli_close($conn);
        ?>

        각 약통에 환자를 지정하세요!
        <div class="btn-container">
            <a href="pillbox1.php" class="btn-3d blue">1번 약통</a>
            <a href="pillbox2.php" class="btn-3d blue">2번 약통</a>
        </div>
        <div class="btn-container">
            <a href="iv.php" class="btn-3d blue">수액팩 남은 양 보기</a>
        </div>
        </CENTER>
    </body>
</html>